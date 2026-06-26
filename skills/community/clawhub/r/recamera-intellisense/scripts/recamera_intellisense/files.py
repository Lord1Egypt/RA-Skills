"""Daemon file API + intellisense events (``/api/v1/file``, ``/api/v1/intellisense/events``)."""

from __future__ import annotations

import base64
from typing import Any, Dict, List, Optional, Union

from . import _config, _http
from ._errors import RecameraError

__all__ = [
    "fetch_file",
    "delete_file",
    "get_intellisense_events",
    "clear_intellisense_events",
]

PATH_FILE = "/api/v1/file"
PATH_EVENTS = "/api/v1/intellisense/events"
PATH_EVENTS_CLEAR = "/api/v1/intellisense/events/clear"
_MAX_INLINE_BYTES = 5 * 1024 * 1024
_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def _validate_absolute_path(path: Any) -> str:
    """Reject obviously unsafe inputs before sending them to the daemon.

    The daemon enforces its own allowlist, but validating here catches
    typos, accidental path traversal (``..``), NUL-byte injection into the
    query string, and non-absolute paths with a clearer error.
    """
    if not isinstance(path, str) or not path:
        raise ValueError("'path' must be a non-empty string.")
    if "\x00" in path:
        raise ValueError("'path' must not contain NUL bytes.")
    if not path.startswith("/"):
        raise ValueError(f"'path' must be an absolute (POSIX) path; got {path!r}.")
    # Normalize and ensure no traversal escapes the absolute root.
    segments = [s for s in path.split("/") if s not in ("", ".")]
    if any(s == ".." for s in segments):
        raise ValueError(f"'path' must not contain '..' segments; got {path!r}.")
    return path


def fetch_file(
    device_name: str,
    *,
    path: str,
    max_inline_bytes: int = _MAX_INLINE_BYTES,
    raw: bool = False,
) -> Union[bytes, Dict[str, Any]]:
    """Fetch an on-device file.

    Returns inline base64 for images / payloads ≤ ``max_inline_bytes``.
    When ``raw=True``, returns the raw ``bytes`` (useful for pipelines).
    """
    path = _validate_absolute_path(path)
    dev = _config.resolve(device_name)
    body, ct = _http.get_bytes(dev, PATH_FILE, params={"path": path})
    if raw:
        return body
    is_image = any(path.lower().endswith(ext) for ext in _IMAGE_EXT)
    if is_image or len(body) <= max_inline_bytes:
        return {
            "path": path,
            "content_type": ct,
            "size": len(body),
            "content_base64": base64.b64encode(body).decode("ascii"),
        }
    return {
        "path": path,
        "content_type": ct,
        "size": len(body),
        "note": "payload exceeds inline budget; re-fetch with a higher max_inline_bytes "
        "or use the MCP streaming transport for large blobs.",
    }


def delete_file(device_name: str, *, path: str) -> None:
    """Delete an on-device file via the daemon."""
    path = _validate_absolute_path(path)
    dev = _config.resolve(device_name)
    _http.delete(dev, PATH_FILE, params={"path": path})


def get_intellisense_events(
    device_name: str,
    *,
    start_unix_ms: Optional[int] = None,
    end_unix_ms: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Fetch raw intellisense events from the daemon event store.

    The daemon accepts ``?start=<ms>&end=<ms>`` (inclusive Unix milliseconds).
    Callers who want the normalized detection-event shape should use
    :func:`detection.get_detection_events` instead.
    """
    dev = _config.resolve(device_name)
    params: Dict[str, Any] = {}
    if start_unix_ms is not None:
        params["start"] = int(start_unix_ms)
    if end_unix_ms is not None:
        params["end"] = int(end_unix_ms)
    data = _http.get_json(dev, PATH_EVENTS, params=params or None)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("events"), list):
        return data["events"]
    return []


def clear_intellisense_events(device_name: str) -> None:
    """Clear all buffered intellisense events on the daemon.

    Calls ``POST /api/v1/intellisense/events/clear`` (the daemon does not
    support ``DELETE`` on the events collection).
    """
    dev = _config.resolve(device_name)
    resp = _http.post_json(dev, PATH_EVENTS_CLEAR)
    if isinstance(resp, dict):
        status = str(resp.get("status", "")).lower()
        if status and status != "ok":
            raise RecameraError(
                f"clear intellisense events failed: {resp.get('message', status)!r}"
            )


COMMANDS = {
    "fetch_file": fetch_file,
    "delete_file": delete_file,
    "get_intellisense_events": get_intellisense_events,
    "clear_intellisense_events": clear_intellisense_events,
}
COMMAND_SCHEMAS = {
    "fetch_file": {
        "required": {"device_name", "path"},
        "optional": {"max_inline_bytes"},
    },
    "delete_file": {"required": {"device_name", "path"}, "optional": set()},
    "get_intellisense_events": {
        "required": {"device_name"},
        "optional": {"start_unix_ms", "end_unix_ms"},
    },
    "clear_intellisense_events": {"required": {"device_name"}, "optional": set()},
}
