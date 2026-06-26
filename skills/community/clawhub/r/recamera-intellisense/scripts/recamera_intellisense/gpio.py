"""GPIO pins: list / info / read / write (auto-configures direction on first use)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = ["list_gpios", "get_gpio_info", "set_gpio_value", "get_gpio_value"]

_BASE = "/api/v1"
_OUTPUT_STATE = "push-pull"
_INPUT_STATE = "floating"
_OUTPUT_STATES = {"push-pull", "open-drain", "open-source"}
_INPUT_STATES = {"floating", "pull-up", "pull-down"}
_DEBOUNCE_MS_DEFAULT = 100


def _parse_info(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": d.get("name", ""),
        "chip": d.get("chip", ""),
        "line": int(d.get("line", 0) or 0),
        "capabilities": list(d.get("capabilities") or []),
    }


def _parse_settings(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "state": d.get("state", "disabled"),
        "edge": d.get("edge", "none"),
        "debounce_ms": int(d.get("debounce_ms", 0) or 0),
    }


def _parse_descriptor(pin_id: int, d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "pin_id": pin_id,
        "info": _parse_info(d.get("info") or {}),
        "settings": _parse_settings(d.get("settings") or {}),
    }


def list_gpios(device_name: str) -> List[Dict[str, Any]]:
    """List all GPIO pins with info + current settings."""
    dev = _config.resolve(device_name)
    data = _http.get_json(dev, f"{_BASE}/gpios") or {}
    out: List[Dict[str, Any]] = []
    for key, val in data.items():
        try:
            pin_id = int(key)
        except (TypeError, ValueError):
            continue
        if isinstance(val, dict):
            out.append(_parse_descriptor(pin_id, val))
    out.sort(key=lambda d: d["pin_id"])
    return out


def get_gpio_info(device_name: str, *, pin_id: int) -> Dict[str, Any]:
    """Return info + settings for *pin_id*."""
    dev = _config.resolve(device_name)
    data = _http.get_json(dev, f"{_BASE}/gpio/{int(pin_id)}") or {}
    return _parse_descriptor(int(pin_id), data)


def _get_settings(dev, pin_id: int) -> Dict[str, Any]:
    data = _http.get_json(dev, f"{_BASE}/gpio/{pin_id}/settings") or {}
    return _parse_settings(data)


def _ensure_output(dev, pin_id: int) -> None:
    s = _get_settings(dev, pin_id)
    if s["state"] in _OUTPUT_STATES:
        return
    _http.post_json(
        dev, f"{_BASE}/gpio/{pin_id}/settings", payload={"state": _OUTPUT_STATE}
    )


def _ensure_input(dev, pin_id: int, debounce_ms: Optional[int]) -> None:
    s = _get_settings(dev, pin_id)
    state_ok = s["state"] in _INPUT_STATES
    debounce_ok = debounce_ms is None or s["debounce_ms"] == int(debounce_ms)
    if state_ok and debounce_ok:
        return
    payload: Dict[str, Any] = {}
    if not state_ok:
        payload["state"] = _INPUT_STATE
    if debounce_ms is not None and not debounce_ok:
        payload["debounce_ms"] = int(debounce_ms)
        # Device rejects debounce when edge=none; enable both-edge detection.
        if int(debounce_ms) > 0 and s.get("edge", "none") == "none":
            payload["edge"] = "both"
    _http.post_json(dev, f"{_BASE}/gpio/{pin_id}/settings", payload=payload)


def set_gpio_value(device_name: str, *, pin_id: int, value: int) -> int:
    """Drive *pin_id* to 0 or 1.

    Reconfigures the pin as a push-pull output first if it is not already in an
    output state — this has the side effect of changing the pin's direction.
    """
    if value not in (0, 1):
        raise ValueError(f"GPIO value must be 0 or 1, got {value}")
    dev = _config.resolve(device_name)
    pin_id = int(pin_id)
    _ensure_output(dev, pin_id)
    _http.post_text(dev, f"{_BASE}/gpio/{pin_id}/value", str(value))
    return value


def get_gpio_value(
    device_name: str,
    *,
    pin_id: int,
    debounce_ms: Optional[int] = _DEBOUNCE_MS_DEFAULT,
) -> int:
    """Read *pin_id* as a 0/1 integer.

    Reconfigures the pin as a floating input first if it is not already in an
    input state — this has the side effect of changing the pin's direction.
    When ``debounce_ms > 0`` and the current edge is ``none``, the SDK also
    enables both-edge detection (the device rejects debounce with edge=none).
    """
    dev = _config.resolve(device_name)
    pin_id = int(pin_id)
    _ensure_input(dev, pin_id, debounce_ms)
    body, _ = _http.get_bytes(dev, f"{_BASE}/gpio/{pin_id}/value")
    text = body.decode("utf-8", errors="replace").strip()
    try:
        return int(text)
    except ValueError as exc:
        raise RecameraError(f"Unexpected GPIO value payload: {text!r}") from exc


COMMANDS = {
    "list_gpios": list_gpios,
    "get_gpio_info": get_gpio_info,
    "set_gpio_value": set_gpio_value,
    "get_gpio_value": get_gpio_value,
}
COMMAND_SCHEMAS = {
    "list_gpios": {"required": {"device_name"}, "optional": set()},
    "get_gpio_info": {"required": {"device_name", "pin_id"}, "optional": set()},
    "set_gpio_value": {
        "required": {"device_name", "pin_id", "value"},
        "optional": set(),
    },
    "get_gpio_value": {
        "required": {"device_name", "pin_id"},
        "optional": {"debounce_ms"},
    },
}
