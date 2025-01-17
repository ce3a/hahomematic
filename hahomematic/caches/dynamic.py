"""Module for the dynamic caches."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any, Final

from hahomematic import central as hmcu
from hahomematic.const import (
    INIT_DATETIME,
    MAX_CACHE_AGE,
    NO_CACHE_ENTRY,
    CallSource,
    InterfaceName,
)
from hahomematic.platforms.device import HmDevice
from hahomematic.support import get_device_address, updated_within_seconds

_LOGGER: Final = logging.getLogger(__name__)


class DeviceDetailsCache:
    """Cache for device/channel details."""

    def __init__(self, central: hmcu.CentralUnit) -> None:
        """Init the device details cache."""
        self._central: Final = central
        self._channel_rooms: Final[dict[str, set[str]]] = {}
        self._device_channel_ids: Final[dict[str, str]] = {}
        self._device_room: Final[dict[str, str]] = {}
        self._functions: Final[dict[str, set[str]]] = {}
        self._interface_cache: Final[dict[str, str]] = {}
        self._names_cache: Final[dict[str, str]] = {}
        self._last_updated = INIT_DATETIME

    async def load(self) -> None:
        """Fetch names from backend."""
        if updated_within_seconds(last_update=self._last_updated, max_age=(MAX_CACHE_AGE / 2)):
            return
        self.clear()
        _LOGGER.debug("load: Loading names for %s", self._central.name)
        if client := self._central.primary_client:
            await client.fetch_device_details()
        _LOGGER.debug("load: Loading rooms for %s", self._central.name)
        self._channel_rooms.clear()
        self._channel_rooms.update(await self._get_all_rooms())
        self._identify_device_room()
        _LOGGER.debug("load: Loading functions for %s", self._central.name)
        self._functions.clear()
        self._functions.update(await self._get_all_functions())
        self._last_updated = datetime.now()

    @property
    def device_channel_ids(self) -> dict[str, str]:
        """Return device channel ids."""
        return self._device_channel_ids

    def add_name(self, address: str, name: str) -> None:
        """Add name to cache."""
        if address not in self._names_cache:
            self._names_cache[address] = name

    def get_name(self, address: str) -> str | None:
        """Get name from cache."""
        return self._names_cache.get(address)

    def add_interface(self, address: str, interface: str) -> None:
        """Add interface to cache."""
        if address not in self._interface_cache:
            self._interface_cache[address] = interface

    def get_interface(self, address: str) -> str:
        """Get interface from cache."""
        return self._interface_cache.get(address) or InterfaceName.BIDCOS_RF

    def add_device_channel_id(self, address: str, channel_id: str) -> None:
        """Add channel id for a channel."""
        self._device_channel_ids[address] = channel_id

    async def _get_all_rooms(self) -> dict[str, set[str]]:
        """Get all rooms, if available."""
        if client := self._central.primary_client:
            return await client.get_all_rooms()
        return {}

    def get_room(self, device_address: str) -> str | None:
        """Return room by device_address."""
        return self._device_room.get(device_address)

    async def _get_all_functions(self) -> dict[str, set[str]]:
        """Get all functions, if available."""
        if client := self._central.primary_client:
            return await client.get_all_functions()
        return {}

    def get_function_text(self, address: str) -> str | None:
        """Return function by address."""
        if functions := self._functions.get(address):
            return ",".join(functions)
        return None

    def remove_device(self, device: HmDevice) -> None:
        """Remove name from cache."""
        if device.device_address in self._names_cache:
            del self._names_cache[device.device_address]
        for channel_address in device.channels:
            if channel_address in self._names_cache:
                del self._names_cache[channel_address]

    def clear(self) -> None:
        """Clear the cache."""
        self._names_cache.clear()
        self._channel_rooms.clear()
        self._functions.clear()
        self._last_updated = INIT_DATETIME

    def _identify_device_room(self) -> None:
        """
        Identify a possible room of a device.

        A room is relevant for a device, if there is only one room assigned to the channels.
        """
        device_rooms: dict[str, set[str]] = {}
        for address, rooms in self._channel_rooms.items():
            if (device_address := get_device_address(address=address)) not in device_rooms:
                device_rooms[device_address] = set()
            device_rooms[device_address].update(rooms)
        for device_address, rooms in device_rooms.items():
            if rooms and len(set(rooms)) == 1:
                self._device_room[device_address] = list(set(rooms))[0]


class CentralDataCache:
    """Central cache for device/channel initial data."""

    def __init__(self, central: hmcu.CentralUnit) -> None:
        """Init the central data cache."""
        self._central: Final = central
        # { key, value}
        self._value_cache: Final[dict[str, Any]] = {}
        self._last_updated = INIT_DATETIME

    @property
    def is_empty(self) -> bool:
        """Return if cache is empty."""
        if len(self._value_cache) == 0:
            return True
        if not updated_within_seconds(last_update=self._last_updated):
            self.clear()
            return True
        return False

    async def load(self) -> None:
        """Fetch data from backend."""
        if updated_within_seconds(last_update=self._last_updated, max_age=(MAX_CACHE_AGE / 2)):
            return
        self.clear()
        _LOGGER.debug("load: device data for %s", self._central.name)
        for client in self._central.clients:
            await client.fetch_all_device_data()

    async def refresh_entity_data(self, paramset_key: str | None = None) -> None:
        """Refresh entity data."""
        for entity in self._central.get_readable_generic_entities(paramset_key=paramset_key):
            await entity.load_entity_value(call_source=CallSource.HM_INIT)

    def add_data(self, all_device_data: dict[str, Any]) -> None:
        """Add data to cache."""
        self._value_cache.update(all_device_data)
        self._last_updated = datetime.now()

    def get_data(
        self,
        interface: str,
        channel_address: str,
        parameter: str,
    ) -> Any:
        """Get data from cache."""
        if not self.is_empty:
            key = f"{interface}.{channel_address.replace(':','%3A')}.{parameter}"
            return self._value_cache.get(key, NO_CACHE_ENTRY)
        return NO_CACHE_ENTRY

    def clear(self) -> None:
        """Clear the cache."""
        self._value_cache.clear()
        self._last_updated = INIT_DATETIME
