"""Storage relay lifecycle + per-process UUID cache (serves record files via nginx autoindex).

This module is **internal**: the relay is an implementation detail of ``records`` and
``files`` (where it is opened/refreshed lazily). It is intentionally not exposed via the
MCP tool surface or the SDK's public CLI command set. Import from Python is still
supported for advanced users who need direct relay control.
"""

from __future__ import annotations

import threading
from typing import Any, Dict, Optional

from . import _config, _http
from .storage import PATH_CONTROL, DEFAULT_INTERNAL_DEV_PATH, get_storage_status

__all__ = [
    "open_relay",
    "get_relay_status",
    "close_relay",
    "resolve_slot_dev_path",
    "ensure_relay_uuid",
    "build_relay_url",
]


def _relay_call(device, action: str, dev_path: str) -> Dict[str, Any]:
    resp = _http.post_json(
        device,
        PATH_CONTROL,
        payload={"sTask": "SYNC", "sAction": action, "sSlotDevPath": dev_path},
    )
    _http.expect_ok(resp, f"storage control {action}")
    return resp if isinstance(resp, dict) else {}


def _extract_relay_status(resp: Dict[str, Any]) -> Dict[str, Any]:
    r = resp.get("dRelayStatus") or {}
    return {
        "uuid": r.get("sRelayDirectory", "") or "",
        "timeout": int(r.get("iRelayTimeout", 0) or 0),
        "timeout_remain": int(r.get("iRelayTimeoutRemain", 0) or 0),
    }


def resolve_slot_dev_path(device_name: str, dev_path: Optional[str] = None) -> str:
    """Return *dev_path* if given, otherwise the first enabled slot (falling back to internal)."""
    if dev_path:
        return dev_path
    slots = get_storage_status(device_name)
    for s in slots:
        if s["enabled"]:
            return s["dev_path"]
    for s in slots:
        if s["dev_path"] == DEFAULT_INTERNAL_DEV_PATH:
            return s["dev_path"]
    raise ValueError(
        "No storage slot available; enable one with set_storage_slot first."
    )


def open_relay(device_name: str, *, dev_path: Optional[str] = None) -> Dict[str, Any]:
    """Open (or refresh) the relay directory; returns ``{uuid, timeout, timeout_remain}``."""
    dev = _config.resolve(device_name)
    resolved = resolve_slot_dev_path(device_name, dev_path)
    resp = _relay_call(dev, "RELAY", resolved)
    status = _extract_relay_status(resp)
    _cache_set(device_name, resolved, status["uuid"])
    return status


def get_relay_status(
    device_name: str, *, dev_path: Optional[str] = None
) -> Dict[str, Any]:
    """Query the current relay status without re-opening."""
    dev = _config.resolve(device_name)
    resolved = resolve_slot_dev_path(device_name, dev_path)
    resp = _relay_call(dev, "RELAY_STATUS", resolved)
    return _extract_relay_status(resp)


def close_relay(device_name: str, *, dev_path: Optional[str] = None) -> None:
    """Close the relay and evict the cached UUID."""
    dev = _config.resolve(device_name)
    resolved = resolve_slot_dev_path(device_name, dev_path)
    resp = _http.post_json(
        dev,
        PATH_CONTROL,
        payload={"sTask": "SYNC", "sAction": "UNRELAY", "sSlotDevPath": resolved},
    )
    _http.expect_ok(resp, "close relay")
    _cache_evict(device_name, resolved)


_CACHE_LOCK = threading.Lock()
_CACHE: Dict[tuple, str] = {}


def _cache_get(device_name: str, dev_path: str) -> Optional[str]:
    with _CACHE_LOCK:
        return _CACHE.get((device_name, dev_path))


def _cache_set(device_name: str, dev_path: str, uuid: str) -> None:
    with _CACHE_LOCK:
        _CACHE[(device_name, dev_path)] = uuid


def _cache_evict(device_name: str, dev_path: str) -> None:
    with _CACHE_LOCK:
        _CACHE.pop((device_name, dev_path), None)


def ensure_relay_uuid(
    device_name: str, dev_path: Optional[str] = None
) -> tuple[str, str]:
    """Return ``(dev_path, uuid)`` for an active relay, opening/renewing one as needed."""
    resolved = resolve_slot_dev_path(device_name, dev_path)
    cached = _cache_get(device_name, resolved)
    if cached:
        try:
            status = get_relay_status(device_name, dev_path=resolved)
            if status["uuid"] and status["timeout_remain"] > 0:
                return resolved, cached
        except Exception:
            pass
        _cache_evict(device_name, resolved)
    status = open_relay(device_name, dev_path=resolved)
    return resolved, status["uuid"]


def build_relay_url(device_name: str, uuid: str, rel_path: str = "") -> str:
    """Construct a direct ``<base>/storage/relay/{uuid}/{rel}`` URL."""
    dev = _config.resolve(device_name)
    rel = rel_path.lstrip("/")
    endpoint = f"/storage/relay/{uuid}/" if not rel else f"/storage/relay/{uuid}/{rel}"
    return _http.base_url(dev) + endpoint


COMMANDS: Dict[str, Any] = {}
COMMAND_SCHEMAS: Dict[str, Any] = {}
