"""Module for HaHomematic generic platforms."""
from __future__ import annotations

import logging
from typing import Any, Final

from hahomematic import support as hms
from hahomematic.const import (
    CLICK_EVENTS,
    VIRTUAL_REMOTE_TYPES,
    Description,
    Operations,
    ParameterType,
)
from hahomematic.platforms import device as hmd
from hahomematic.platforms.generic import entity as hmge
from hahomematic.platforms.generic.action import HmAction
from hahomematic.platforms.generic.binary_sensor import HmBinarySensor
from hahomematic.platforms.generic.button import HmButton
from hahomematic.platforms.generic.number import HmFloat, HmInteger
from hahomematic.platforms.generic.select import HmSelect
from hahomematic.platforms.generic.sensor import HmSensor
from hahomematic.platforms.generic.switch import HmSwitch
from hahomematic.platforms.generic.text import HmText
from hahomematic.platforms.support import generate_unique_identifier, is_binary_sensor

_LOGGER: Final = logging.getLogger(__name__)
_BUTTON_ACTIONS: Final[tuple[str, ...]] = ("RESET_MOTION", "RESET_PRESENCE")


def create_entity_and_append_to_device(
    device: hmd.HmDevice,
    channel_address: str,
    paramset_key: str,
    parameter: str,
    parameter_data: dict[str, Any],
) -> None:
    """Decides which default platform should be used, and creates the required entities."""
    if device.central.parameter_visibility.parameter_is_ignored(
        device_type=device.device_type,
        channel_no=hms.get_channel_no(address=channel_address),
        paramset_key=paramset_key,
        parameter=parameter,
    ):
        _LOGGER.debug(
            "CREATE_ENTITIES: Ignoring parameter: %s [%s]",
            parameter,
            channel_address,
        )
        return

    unique_identifier = generate_unique_identifier(
        central=device.central, address=channel_address, parameter=parameter
    )
    if device.central.has_entity(unique_identifier=unique_identifier):
        _LOGGER.debug(
            "CREATE_ENTITIES: Skipping %s (already exists)",
            unique_identifier,
        )
        return
    _LOGGER.debug(
        "CREATE_ENTITIES: Creating entity for %s, %s, %s",
        channel_address,
        parameter,
        device.interface_id,
    )
    p_type = parameter_data[Description.TYPE]
    p_operations = parameter_data[Description.OPERATIONS]
    entity_t: type[hmge.GenericEntity] | None = None
    if p_operations & Operations.WRITE:
        if p_type == ParameterType.ACTION:
            if p_operations == Operations.WRITE:
                if parameter in _BUTTON_ACTIONS or device.device_type in VIRTUAL_REMOTE_TYPES:
                    entity_t = HmButton
                else:
                    entity_t = HmAction
            elif parameter in CLICK_EVENTS:
                entity_t = HmButton
            else:
                entity_t = HmSwitch
        elif p_operations == Operations.WRITE:
            entity_t = HmAction
        elif p_type == ParameterType.BOOL:
            entity_t = HmSwitch
        elif p_type == ParameterType.ENUM:
            entity_t = HmSelect
        elif p_type == ParameterType.FLOAT:
            entity_t = HmFloat
        elif p_type == ParameterType.INTEGER:
            entity_t = HmInteger
        elif p_type == ParameterType.STRING:
            entity_t = HmText
    elif parameter not in CLICK_EVENTS:
        # Also check, if sensor could be a binary_sensor due to value_list.
        if is_binary_sensor(parameter_data):
            parameter_data[Description.TYPE] = ParameterType.BOOL
            entity_t = HmBinarySensor
        else:
            entity_t = HmSensor

    if entity_t:
        entity = entity_t(
            device=device,
            unique_identifier=unique_identifier,
            channel_address=channel_address,
            paramset_key=paramset_key,
            parameter=parameter,
            parameter_data=parameter_data,
        )
        _LOGGER.debug(
            "CREATE_ENTITY_AND_APPEND_TO_DEVICE: %s: %s %s",
            entity.platform,
            channel_address,
            parameter,
        )
        device.add_entity(entity)
        if new_platform := device.central.parameter_visibility.wrap_entity(wrapped_entity=entity):
            wrapper_entity = hmge.WrapperEntity(wrapped_entity=entity, new_platform=new_platform)
            device.add_entity(wrapper_entity)
