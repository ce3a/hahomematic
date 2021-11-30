"""
Constants used by hahomematic.
"""
from __future__ import annotations

DEFAULT_ENCODING = "UTF-8"

LOCALHOST = "localhost"
IP_LOCALHOST_V4 = "127.0.0.1"
IP_LOCALHOST_V6 = "::1"
IP_ANY_V4 = "0.0.0.0"
IP_ANY_V6 = "::"
PORT_ANY = 0

PORT_GROUPS_NAME = "groups"
PORT_GROUPS = 9292
PORT_GROUPS_TLS = 49292
PORT_HMIP_NAME = "hmip"
PORT_HMIP = 2010
PORT_HMIP_TLS = 42010
PORT_HS485D_NAME = "hs485d"
PORT_HS485D = 2000
PORT_HS485D_TLS = 42000
PORT_RFD_NAME = "rfd"
PORT_RFD = 2001
PORT_RFD_TLS = 42001

PORT_REGA_HSS_NAME = "rega hss"
PORT_REGA_HSS = 1999
PORT_REGA_HSS_TLS = 41999
PORT_REGA_SCRIPT_NAME = "rega script"
PORT_REGA_SCRIPT = 8181
PORT_REGA_SCRIPT_TLS = 48181

DEFAULT_PORTS = {
    PORT_RFD_NAME: (PORT_RFD, PORT_RFD_TLS),
    PORT_HMIP_NAME: (PORT_HMIP, PORT_HMIP_TLS),
    PORT_GROUPS_NAME: (PORT_GROUPS, PORT_GROUPS_TLS),
    PORT_HS485D_NAME: (PORT_HS485D, PORT_HS485D_TLS),
}

PRIMARY_PORTS = [PORT_HMIP, PORT_HMIP_TLS, PORT_RFD, PORT_RFD_TLS]

PATH_JSON_RPC = "/api/homematic.cgi"
PATH_TCL_REGA = "/tclrega.exe"

FILE_DEVICES_RAW = None
FILE_DEVICES = "homematic_devices.json"
FILE_PARAMSETS = "homematic_paramsets.json"
FILE_NAMES = "homematic_names.json"

PARAMSET_MASTER = "MASTER"
PARAMSET_VALUES = "VALUES"

RELEVANT_PARAMSETS = [
    PARAMSET_VALUES,
    # PARAMSET_MASTER,
]

HA_DOMAIN = "hahm"

HH_EVENT_DELETE_DEVICES = "deleteDevices"
HH_EVENT_DEVICES_CREATED = "devicesCreated"
HH_EVENT_ERROR = "error"
HH_EVENT_LIST_DEVICES = "listDevices"
HH_EVENT_NEW_DEVICES = "newDevices"
HH_EVENT_RE_ADDED_DEVICE = "readdedDevice"
HH_EVENT_REPLACE_DEVICE = "replaceDevice"
HH_EVENT_UPDATE_DEVICE = "updateDevice"

# When CONFIG_PENDING turns from True to False (ONLY then!) we should re fetch the paramsets.
# However, usually multiple of these events are fired, so we should only
# act on the last one. This also only seems to fire on channel 0.
EVENT_CONFIG_PENDING = "CONFIG_PENDING"
EVENT_ERROR = "ERROR"

# Only available on CCU
EVENT_PONG = "PONG"
EVENT_PRESS = "PRESS"
EVENT_PRESS_SHORT = "PRESS_SHORT"
EVENT_PRESS_LONG = "PRESS_LONG"
EVENT_PRESS_CONT = "PRESS_CONT"
EVENT_PRESS_LONG_RELEASE = "PRESS_LONG_RELEASE"
EVENT_PRESS_LONG_START = "PRESS_LONG_START"
EVENT_SEQUENCE_OK = "SEQUENCE_OK"
EVENT_UN_REACH = "UNREACH"

EVENT_ALARM = "homematic.alarm"
EVENT_KEYPRESS = "homematic.keypress"
EVENT_IMPULSE = "homematic.impulse"

CLICK_EVENTS = [
    EVENT_PRESS,
    EVENT_PRESS_SHORT,
    EVENT_PRESS_LONG,
    EVENT_PRESS_CONT,
    EVENT_PRESS_LONG_RELEASE,
    EVENT_PRESS_LONG_START,
]

EVENT_ACOUSTIC_ALARM_ACTIVE = "ACOUSTIC_ALARM_ACTIVE"
EVENT_ALARMSTATE = "ALARMSTATE"
EVENT_DEW_POINT_ALARM = "DEW_POINT_ALARM"
EVENT_HUMIDITY_ALARM = "HUMIDITY_ALARM"
EVENT_MOISTURE_DETECTED = "MOISTURE_DETECTED"
EVENT_OPTICAL_ALARM_ACTIVE = "OPTICAL_ALARM_ACTIVE"
EVENT_SMOKE_DETECTOR_ALARM_STATUS = "SMOKE_DETECTOR_ALARM_STATUS"
EVENT_WATERLEVEL_DETECTED = "WATERLEVEL_DETECTED"

ALARM_EVENTS = [
    EVENT_ACOUSTIC_ALARM_ACTIVE,
    EVENT_ALARMSTATE,
    EVENT_DEW_POINT_ALARM,
    EVENT_HUMIDITY_ALARM,
    EVENT_MOISTURE_DETECTED,
    EVENT_OPTICAL_ALARM_ACTIVE,
    EVENT_SMOKE_DETECTOR_ALARM_STATUS,
    EVENT_WATERLEVEL_DETECTED,
]

IMPULSE_EVENTS = [EVENT_CONFIG_PENDING, EVENT_ERROR, EVENT_SEQUENCE_OK, EVENT_UN_REACH]

PARAM_UN_REACH = "UNREACH"
PARAM_CONFIG_PENDING = "CONFIG_PENDING"

# Parameters within the paramsets for which we create entities.
WHITELIST_PARAMETERS = ["SMOKE_DETECTOR_ALARM_STATUS"]

# Parameters within the paramsets for which we don't create entities.
IGNORED_PARAMETERS = [
    "ACTIVITY_STATE",
    "AES_KEY",
    "BOOST_TIME",
    "BOOT",
    "BURST_LIMIT_WARNING",
    "CLEAR_WINDOW_OPEN_SYMBOL",
    "DATE_TIME_UNKNOWN",
    "DECISION_VALUE",
    "DEVICE_IN_BOOTLOADER",
    "DEW_POINT_ALARM",
    "EMERGENCY_OPERATION",
    "EXTERNAL_CLOCK",
    "FROST_PROTECTION",
    "HEATING_COOLING",
    "HUMIDITY_LIMITER",
    "INCLUSION_UNSUPPORTED_DEVICE",
    "INHIBIT",
    "INSTALL_MODE",
    "LEVEL_REAL",
    "OLD_LEVEL",
    "PARTY_SET_POINT_TEMPERATURE",
    "PARTY_TIME_END",
    "PARTY_TIME_START",
    "PROCESS",
    "QUICK_VETO_TIME",
    "RELOCK_DELAY" "SECTION",
    "SET_SYMBOL_FOR_HEATING_PHASE",
    "STATE_UNCERTAIN",
    "STICKY_UNREACH",
    "SWITCH_POINT_OCCURED",
    "TEMPERATURE_LIMITER",
    "TEMPERATURE_OUT_OF_RANGE",
    "TIME_OF_OPERATION",
    "UPDATE_PENDING",
    "WEEK_PROGRAM_CHANNEL_LOCKS",
    "WOCHENPROGRAMM",
]

IGNORED_PARAMETERS_WILDCARDS_END = [
    "OVERFLOW",
    "OVERHEAT",
    "OVERRUN",
    "REPORTING",
    "RESULT",
    "STATUS",
    "SUBMIT",
    "WORKING",
]
IGNORED_PARAMETERS_WILDCARDS_START = [
    "ADJUSTING",
    "ERROR",
    "PARTY_START",
    "PARTY_STOP",
    "STATUS_FLAG",
]

HIDDEN_PARAMETERS = [PARAM_UN_REACH, PARAM_CONFIG_PENDING]

BACKEND_CCU = "CCU"
BACKEND_HOMEGEAR = "Homegear"
BACKEND_PYDEVCCU = "PyDevCCU"

PROXY_INIT_FAILED = 0
PROXY_INIT_SUCCESS = 1
PROXY_DE_INIT_FAILED = 4
PROXY_DE_INIT_SUCCESS = 8
PROXY_DE_INIT_SKIPPED = 16

DATA_LOAD_SUCCESS = 10
DATA_LOAD_FAIL = 100
DATA_NO_LOAD = 99
DATA_SAVE_SUCCESS = 10
DATA_SAVE_FAIL = 100
DATA_NO_SAVE = 99

ATTR_ADDRESS = "address"
ATTR_CALLBACK_HOST = "callback_host"
ATTR_CALLBACK_PORT = "callback_port"
ATTR_CHANNELS = "channels"
ATTR_ERROR = "error"
ATTR_HOST = "host"
ATTR_INTERFACE = "interface"
ATTR_INTERFACE_ID = "interface_id"
ATTR_IP = "ip"
ATTR_JSON_PORT = "json_port"
ATTR_NAME = "name"
ATTR_PASSWORD = "password"
ATTR_PARAMETER = "parameter"
ATTR_PORT = "port"
ATTR_RESULT = "result"
ATTR_SESSION_ID = "_session_id_"
ATTR_TLS = "tls"
ATTR_TYPE = "type"
ATTR_USERNAME = "username"
ATTR_VALUE = "value"
ATTR_VERIFY_TLS = "verify_tls"

ATTR_HM_ALARM = "ALARM"
ATTR_HM_ADDRESS = "ADDRESS"
ATTR_HM_DEFAULT = "DEFAULT"
ATTR_HM_FIRMWARE = "FIRMWARE"
ATTR_HM_FLAGS = "FLAGS"
ATTR_HM_OPERATIONS = "OPERATIONS"
ATTR_HM_PARAMSETS = "PARAMSETS"
ATTR_HM_TYPE = "TYPE"
ATTR_HM_SUBTYPE = "SUBTYPE"
ATTR_HM_LIST = "LIST"
ATTR_HM_LOGIC = "LOGIC"
ATTR_HM_NAME = "NAME"
ATTR_HM_NUMBER = "NUMBER"
ATTR_HM_UNIT = "UNIT"
ATTR_HM_MAX = "MAX"
ATTR_HM_MIN = "MIN"
# Optional member for TYPE: FLOAT, INTEGER
ATTR_HM_SPECIAL = "SPECIAL"  # Which has the following keys
ATTR_HM_VALUE = "VALUE"  # Float or integer, depending on TYPE
# Members for ENUM
ATTR_HM_VALUE_LIST = "VALUE_LIST"

OPERATION_NONE = 0
OPERATION_READ = 1
OPERATION_WRITE = 2
OPERATION_EVENT = 4

TYPE_FLOAT = "FLOAT"
TYPE_INTEGER = "INTEGER"
TYPE_BOOL = "BOOL"
TYPE_ENUM = "ENUM"
TYPE_STRING = "STRING"
TYPE_ACTION = "ACTION"  # Usually buttons, send Boolean to trigger

FLAG_VISIBLE = 1
FLAG_INTERAL = 2
# FLAG_TRANSFORM = 4 # not used
FLAG_SERVICE = 8
# FLAG_STICKY = 10  # This might be wrong. Documentation says 0x10 # not used

DEFAULT_PASSWORD = None
DEFAULT_PATH = None
DEFAULT_USERNAME = "Admin"
DEFAULT_TIMEOUT = 30
DEFAULT_INIT_TIMEOUT = 90
DEFAULT_TLS = False
DEFAULT_VERIFY_TLS = False

HA_PLATFORM_ACTION = "action"
HA_PLATFORM_BINARY_SENSOR = "binary_sensor"
HA_PLATFORM_BUTTON = "button"
HA_PLATFORM_CLIMATE = "climate"
HA_PLATFORM_COVER = "cover"
HA_PLATFORM_EVENT = "event"
HA_PLATFORM_LIGHT = "light"
HA_PLATFORM_LOCK = "lock"
HA_PLATFORM_NUMBER = "number"
HA_PLATFORM_SELECT = "select"
HA_PLATFORM_SENSOR = "sensor"
HA_PLATFORM_SWITCH = "switch"
HA_PLATFORM_TEXT = "text"

HA_PLATFORMS = [
    HA_PLATFORM_BINARY_SENSOR,
    HA_PLATFORM_BUTTON,
    HA_PLATFORM_CLIMATE,
    HA_PLATFORM_COVER,
    HA_PLATFORM_LIGHT,
    HA_PLATFORM_LOCK,
    HA_PLATFORM_NUMBER,
    HA_PLATFORM_SELECT,
    HA_PLATFORM_SENSOR,
    HA_PLATFORM_SWITCH,
]

HM_ENTITY_UNIT_REPLACE = {'"': "", "100%": "%", "% rF": "%"}

HM_VIRTUAL_REMOTE_HM = "BidCoS-RF"
HM_VIRTUAL_REMOTE_HMIP = "HmIP-RCV-1"
HM_VIRTUAL_REMOTES = [HM_VIRTUAL_REMOTE_HM, HM_VIRTUAL_REMOTE_HMIP]
