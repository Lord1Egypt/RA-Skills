"""Device system endpoints: info, resources, time, reboot (`/system/...`)."""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

from typing import Any, Dict, Optional

from . import _config, _http
from ._coerce import require_confirm

__all__ = ["get_device_info", "get_resource_info", "get_system_time",
           "get_battery_status", "reboot_device"]

PATH_DEVICE_INFO = "/cgi-bin/entry.cgi/system/device-info"
PATH_RESOURCE_INFO = "/cgi-bin/entry.cgi/system/resource-info"
PATH_TIME = "/cgi-bin/entry.cgi/system/time"
PATH_BATTERY = "/cgi-bin/entry.cgi/system/battery"
PATH_REBOOT = "/cgi-bin/entry.cgi/system/reboot"


def get_device_info(device_name: Optional[str] = None) -> Dict[str, Any]:
    """Firmware/hardware identity of the device."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_DEVICE_INFO) or {}
    return {
        "serial_number": d.get("sSerialNumber"),
        "firmware_version": d.get("sFirmwareVersion"),
        "sensor_model": d.get("sSensorModel"),
        "base_plate_model": d.get("sBasePlateModel"),
    }


def _usage_block(d: Dict[str, Any], total: str, used: str, pct: str) -> Dict[str, Any]:
    return {"total_gb": d.get(total), "used_gb": d.get(used), "usage_percent": d.get(pct)}


def get_resource_info(device_name: Optional[str] = None) -> Dict[str, Any]:
    """CPU/NPU/memory/storage utilisation (percentages 0-100)."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_RESOURCE_INFO) or {}
    return {
        "cpu_usage": d.get("iCpuUsage"),
        "npu_usage": d.get("iNpuUsage"),
        "memory": _usage_block(d.get("sMem") or {}, "iMemTotal", "iMemUsed", "iMemUsage"),
        "storage": _usage_block(
            d.get("sStorage") or {}, "iStorageTotal", "iStorageUsed", "iStorageUsage"
        ),
    }


def get_system_time(device_name: Optional[str] = None) -> Dict[str, Any]:
    """Device clock, timezone, and NTP configuration."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_TIME) or {}
    ntp = d.get("dNtpConfig") or {}
    return {
        "method": d.get("sMethod"),
        "timestamp": d.get("iTimestamp"),
        "timezone": d.get("sTimezone"),
        "tz": d.get("sTz"),
        "ntp": {"address": ntp.get("sAddress"), "port": ntp.get("sPort")},
    }


def reboot_device(device_name: Optional[str] = None, *, confirm: bool = False) -> None:
    """Reboot the device. Disruptive: all streams, captures, and sessions drop.

    Requires `confirm=True`.
    """
    require_confirm(confirm, "reboot device")
    dev = _config.resolve(device_name)
    resp = _http.post_json(dev, PATH_REBOOT)
    _http.expect_ok(resp, "reboot device")


def get_battery_status(device_name: Optional[str] = None) -> Dict[str, Any]:
    """Battery/power status: ``{attached, charging, display_steps,
    total_steps}``. ``attached`` is false on base plates without a battery."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_BATTERY) or {}
    return {
        "attached": bool(d.get("isAttached", False)),
        "charging": bool(d.get("isCharging", False)),
        "display_steps": int(d.get("displaySteps", 0)),
        "total_steps": int(d.get("totalSteps", 0)),
    }


COMMANDS = {
    "get_device_info": get_device_info,
    "get_resource_info": get_resource_info,
    "get_system_time": get_system_time,
    "get_battery_status": get_battery_status,
    "reboot_device": reboot_device,
}
