"""
Implementation of an async json-rpc client.
"""
import json
import logging
import ssl

from aiohttp import ClientConnectorError, ClientError, ClientSession, TCPConnector

from hahomematic import config
from hahomematic.const import (
    ATTR_ERROR,
    ATTR_PASSWORD,
    ATTR_RESULT,
    ATTR_SESSION_ID,
    ATTR_USERNAME,
    PATH_JSON_RPC,
)

_LOGGER = logging.getLogger(__name__)
VERIFIED_CTX = ssl.create_default_context()
UNVERIFIED_CTX = ssl.create_default_context()
UNVERIFIED_CTX.check_hostname = False
UNVERIFIED_CTX.verify_mode = ssl.CERT_NONE


class JsonRpcAioHttpClient:
    """Connection to CCU JSON-RPC Server."""

    def __init__(
        self,
        central_config,
    ):
        """Session setup."""
        self._central_config = central_config
        if self._central_config.client_session:
            self._client_session = self._central_config.client_session
        else:
            conn = TCPConnector(limit=3)
            self._client_session = ClientSession(
                connector=conn, loop=self._central_config.loop
            )
        self._session_id = None
        self._host = self._central_config.host
        self._port = self._central_config.json_port
        self._username = self._central_config.username
        self._password = self._central_config.password
        self._json_tls = self._central_config.json_tls
        self._verify_tls = self._central_config.verify_tls
        self._ssl_context = self._get_tls_context()

    def _get_tls_context(self):
        ssl_context = None
        if self._json_tls:
            if self._verify_tls:
                ssl_context = ssl.create_default_context()
            else:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    @property
    def is_activated(self):
        """If session exists, then it is activated."""
        return self._session_id is not None

    async def login_or_renew(self):
        """Renew JSON-RPC session or perform login."""
        if not self.is_activated:
            self._session_id = await self._login()
            return self._session_id is not None

        self._session_id = await self._renew_login(self._session_id)
        return self._session_id is not None

    async def _renew_login(self, session_id) -> str:
        """Renew JSON-RPC session or perform login."""
        try:
            response = await self._post(
                session_id=session_id,
                method="Session.renew",
                extra_params={ATTR_SESSION_ID: session_id},
            )
            if response[ATTR_ERROR] is None and response[ATTR_RESULT]:
                return response[ATTR_RESULT]
            return await self._login()
        except ClientError:
            _LOGGER.exception(
                "json_rpc.renew: Exception while renewing JSON-RPC session."
            )
            return None

    async def _login(self) -> str:
        """Login to CCU and return session."""
        session_id = False
        try:
            params = {
                ATTR_USERNAME: self._username,
                ATTR_PASSWORD: self._password,
            }
            response = await self._post(
                session_id=False,
                method="Session.login",
                extra_params=params,
                use_default_params=False,
            )
            if response[ATTR_ERROR] is None and response[ATTR_RESULT]:
                session_id = response[ATTR_RESULT]

            if not session_id:
                _LOGGER.warning(
                    "json_rpc.login: Unable to open session: %s", response[ATTR_ERROR]
                )
                return None
            return session_id
        except Exception:
            _LOGGER.exception("json_rpc.login: Exception while logging in via JSON-RPC")
            return None

    async def post(
        self, method, extra_params=None, use_default_params=True, keep_session=False
    ):
        """Reusable JSON-RPC POST function."""
        if keep_session:
            await self.login_or_renew()
            session_id = self._session_id
        else:
            session_id = await self._login()

        if not session_id:
            _LOGGER.exception("json_rpc.post: Exception while logging in via JSON-RPC.")
            return {"error": "Unable to open session.", "result": {}}

        result = await self._post(
            session_id=session_id,
            method=method,
            extra_params=extra_params,
            use_default_params=use_default_params,
        )

        if not keep_session:
            await self._logout(session_id=session_id)
        return result

    async def _post(
        self, session_id, method, extra_params=None, use_default_params=True
    ):
        """Reusable JSON-RPC POST function."""
        if not self._username:
            no_username = "json_rpc_client._post: No username set."
            _LOGGER.warning(no_username)
            return {"error": str(no_username), "result": {}}
        if not self._password:
            no_password = "json_rpc_client._post: No password set."
            _LOGGER.warning(no_password)
            return {"error": str(no_password), "result": {}}

        params = _get_params(session_id, extra_params, use_default_params)

        _LOGGER.debug("json_rpc_client._post: Method: %s", method)
        try:
            payload = json.dumps(
                {"method": method, "params": params, "jsonrpc": "1.1", "id": 0}
            ).encode("utf-8")

            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(payload)),
            }

            _LOGGER.debug("json_rpc_client._post: API-Endpoint: %s", self._url)
            if self._json_tls:
                resp = await self._client_session.post(
                    self._url,
                    data=payload,
                    headers=headers,
                    timeout=config.TIMEOUT,
                    ssl=self._ssl_context,
                )
            else:
                resp = await self._client_session.post(
                    self._url, data=payload, headers=headers, timeout=config.TIMEOUT
                )
            if resp.status == 200:
                try:
                    return await resp.json(encoding="utf-8")
                except ValueError:
                    _LOGGER.exception(
                        "json_rpc_client._post: Failed to parse JSON. Trying workaround."
                    )
                    # Workaround for bug in CCU
                    return json.loads(
                        await resp.json(encoding="utf-8").replace("\\", "")
                    )
            else:
                _LOGGER.error("json_rpc_client._post: Status: %i", resp.status)
                return {"error": resp.status, "result": {}}
        except ClientConnectorError as err:
            _LOGGER.exception("json_rpc_client._post: ClientConnectorError")
            return {"error": str(err), "result": {}}
        except ClientError as cce:
            _LOGGER.exception("json_rpc_client._post: ClientError")
            return {"error": str(cce), "result": {}}
        except TypeError as ter:
            _LOGGER.exception("json_rpc_client._post: TypeError")
            return {"error": str(ter), "result": {}}

    async def logout(self):
        """Logout of CCU."""
        await self._logout(self._session_id)

    async def _logout(self, session_id):
        """Logout of CCU."""
        if not session_id:
            _LOGGER.warning("json_rpc.logout: Not logged in. Not logging out.")
            return
        try:
            params = {"_session_id_": session_id}
            response = await self._post(
                session_id=session_id,
                method="Session.logout",
                extra_params=params,
            )
            if response[ATTR_ERROR]:
                _LOGGER.warning(
                    "json_rpc.logout: Logout error: %s", response[ATTR_RESULT]
                )
        except ClientError:
            _LOGGER.exception(
                "json_rpc.logout: Exception while logging in via JSON-RPC"
            )
        return

    @property
    def _url(self):
        """Return the required url."""
        url = "http://"
        if self._json_tls:
            url = "https://"
        url = f"{url}{self._host}"
        if self._port:
            url = f"{url}:{self._port}"
        return f"{url}{PATH_JSON_RPC}"


def _get_params(session_id, extra_params, use_default_params) -> dict[str, str]:
    """Add additional params to default prams."""
    params = {"_session_id_": session_id} if use_default_params else {}
    if extra_params:
        params.update(extra_params)
    return params
