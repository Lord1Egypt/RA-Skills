"""Stdlib-only Python SDK for reCamera; shares `~/.recamera/devices.json` with the MCP server."""

from __future__ import annotations

from ._errors import RecameraError
from .acoustic import (get_active_acoustic_model, list_acoustic_models,
                       set_acoustic_model)
from .apps import (get_app_logs, list_apps, restart_app, start_app,
                    stop_app)
from .backup import export_device_config
from .capture import capture_image, get_capture_status, start_capture, stop_capture
from .notify import get_notify_config, set_notify_config
from .video import get_video_encode, set_video_encode
from .detection import (
    clear_detection_events,
    get_detection_events,
    get_detection_rules,
    get_detection_schedule,
    set_detection_rules,
    set_detection_schedule,
)
from .device import (
    add_device,
    detect_local_device,
    get_device,
    list_devices,
    remove_device,
    update_device,
)
from .files import (
    clear_intellisense_events,
    delete_file,
    fetch_file,
    get_intellisense_events,
)
from .gpio import get_gpio_info, get_gpio_value, list_gpios, set_gpio_value
from .image import get_image_settings, set_image_settings
from .model import get_detection_model, get_detection_models_info, set_detection_model
from .records import fetch_record, list_records
from .relay import close_relay, get_relay_status, open_relay
from .rule import (
    activate_http_trigger,
    get_record_config,
    get_record_sources,
    get_record_trigger,
    get_rule_system_info,
    get_schedule_rule,
    set_record_config,
    set_record_trigger,
    set_schedule_rule,
)
from .storage import (
    configure_storage_quota,
    get_storage_status,
    set_storage_slot,
    storage_task_cancel,
    storage_task_status,
    storage_task_submit,
)
from .system import (
    get_battery_status,
    get_device_info,
    get_resource_info,
    get_system_time,
    reboot_device,
)

__version__ = "2.3.0"

__all__ = [
    "RecameraError",
    # device
    "detect_local_device",
    "add_device",
    "update_device",
    "remove_device",
    "get_device",
    "list_devices",
    # rule system
    "get_rule_system_info",
    "get_record_config",
    "set_record_config",
    "get_schedule_rule",
    "set_schedule_rule",
    "get_record_trigger",
    "get_record_sources",
    "set_record_trigger",
    "activate_http_trigger",
    # storage
    "get_storage_status",
    "set_storage_slot",
    "configure_storage_quota",
    "storage_task_submit",
    "storage_task_status",
    "storage_task_cancel",
    # records
    "list_records",
    "fetch_record",
    # capture
    "get_capture_status",
    "start_capture",
    "stop_capture",
    "capture_image",
    # gpio
    "list_gpios",
    "get_gpio_info",
    "set_gpio_value",
    "get_gpio_value",
    # acoustic
    "get_active_acoustic_model",
    "list_acoustic_models",
    "set_acoustic_model",
    # app center / video / notify / backup
    "list_apps",
    "start_app",
    "stop_app",
    "restart_app",
    "get_app_logs",
    "get_video_encode",
    "set_video_encode",
    "get_notify_config",
    "set_notify_config",
    "export_device_config",
    # model / detection
    "get_detection_models_info",
    "get_detection_model",
    "set_detection_model",
    "get_detection_schedule",
    "set_detection_schedule",
    "get_detection_rules",
    "set_detection_rules",
    "get_detection_events",
    "clear_detection_events",
    # daemon files
    "fetch_file",
    "delete_file",
    "get_intellisense_events",
    "clear_intellisense_events",
    # system / image
    "get_device_info",
    "get_resource_info",
    "get_system_time",
    "get_battery_status",
    "reboot_device",
    "get_image_settings",
    "set_image_settings",
    # relay helpers (advanced; managed automatically by records)
    "open_relay",
    "get_relay_status",
    "close_relay",
]
