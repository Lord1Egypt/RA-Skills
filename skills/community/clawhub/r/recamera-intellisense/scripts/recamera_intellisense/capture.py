"""Capture status, start/stop, and the ``capture_image`` helper."""

from __future__ import annotations

import base64
import time
from typing import Any, Dict, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = ["get_capture_status", "start_capture", "stop_capture", "capture_image"]

PATH_STATUS = "/cgi-bin/entry.cgi/record/capture/status"
PATH_START = "/cgi-bin/entry.cgi/record/capture/start"
PATH_STOP = "/cgi-bin/entry.cgi/record/capture/stop"

FORMAT_IMAGE = "JPG"
OUTPUT_FALLBACK = "/mnt/rc_mmcblk0p8/reCamera"
_POLL_INTERVAL_S = 0.5
_DEFAULT_TIMEOUT_S = 5.0
_TERMINAL = {"COMPLETED", "FAILED", "INTERRUPTED", "CANCELED"}


def _parse_event(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": d.get("sID", ""),
        "output_directory": d.get("sOutputDirectory", ""),
        "format": d.get("sFormat", ""),
        "video_length_seconds": d.get("iVideoLengthSeconds"),
        "status": d.get("sStatus", "UNKNOWN"),
        "timestamp_unix_ms": int(d.get("iTimestamp", 0) or 0),
        "file_name": d.get("sFileName", ""),
    }


def get_capture_status(device_name: str) -> Dict[str, Any]:
    """Current capture state (includes the last event, if any)."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_STATUS) or {}
    last = d.get("dLastCapture")
    return {
        "last_capture": _parse_event(last) if isinstance(last, dict) else None,
        "ready_to_start_new": bool(d.get("bReadyToStartNew", False)),
        "stop_requested": bool(d.get("bStopRequested", False)),
    }


def _validate_output_dir(output: Optional[str]) -> Optional[str]:
    """Validate that ``output`` is an absolute on-device directory path.

    ``sOutput`` is the directory on the *camera's* filesystem where the
    capture is written (the device supplies the file name); it is **not** a
    local destination. Callers who want the bytes locally should use
    :func:`capture_image` or fetch the resulting file afterwards.
    """
    if output is None:
        return None
    if not isinstance(output, str) or not output.strip():
        raise ValueError("'output' must be a non-empty string.")
    if "\x00" in output:
        raise ValueError("'output' must not contain NUL bytes.")
    if not output.startswith("/"):
        raise ValueError(
            f"'output' must be an absolute on-device directory path; got {output!r}. "
            "Use get_storage_status to find a mount path (e.g. '/mnt/rc_mmcblk0p8/reCamera'), "
            "or omit 'output' to use the selected storage slot."
        )
    return output


def start_capture(
    device_name: str,
    *,
    output: Optional[str] = None,
    format: str = FORMAT_IMAGE,
    video_length_seconds: Optional[int] = None,
) -> Dict[str, Any]:
    """Start a capture; returns the initial capture event.

    ``output`` is an **on-device directory** (not a local path). Omit it to
    auto-resolve from the currently selected storage slot. The device picks
    the file name; retrieve the resulting file with :func:`files.fetch_file`
    using the event's ``output_directory`` + ``file_name``.
    """
    output = _validate_output_dir(output)
    dev = _config.resolve(device_name)
    payload: Dict[str, Any] = {
        "sOutput": output or OUTPUT_FALLBACK,
        "sFormat": str(format).upper(),
    }
    if video_length_seconds is not None:
        payload["iVideoLengthSeconds"] = int(video_length_seconds)
    try:
        resp = _http.post_json(dev, PATH_START, payload=payload)
        _http.expect_ok(resp, "start capture")
    except RecameraError as exc:
        # Device rejects paths outside a storage mount (error code 30022).
        # Re-raise with an actionable hint so agents don't retry blindly.
        if exc.code == 30022 or "30022" in str(exc):
            raise RecameraError(
                f"{exc} Hint: 'output' must be an on-device directory under a "
                "mounted storage slot (see get_storage_status for mount_path), "
                "or omit 'output' to use the default.",
                status=exc.status,
                code=exc.code,
                body=exc.body,
            ) from exc
        raise
    capture = resp.get("dCapture")
    if not isinstance(capture, dict):
        raise RecameraError("start_capture response missing dCapture field.")
    return _parse_event(capture)


def stop_capture(device_name: str) -> None:
    """Stop the running capture (no-op for JPG)."""
    dev = _config.resolve(device_name)
    resp = _http.post_json(dev, PATH_STOP)
    _http.expect_ok(resp, "stop capture")


def capture_image(
    device_name: str,
    *,
    output: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT_S,
) -> Dict[str, Any]:
    """Start a JPG capture, poll to completion (terminal states ``COMPLETED/FAILED/INTERRUPTED/CANCELED``),
    fetch the file via the daemon, and return ``{event, path, size, content_base64}``.
    """
    # Resolve output dir via current storage status if not supplied.
    if output is None:
        try:
            from .storage import get_storage_status

            slots = get_storage_status(device_name)
            slot = next((s for s in slots if s["enabled"] and s["mount_path"]), None)
            if slot:
                base = slot["mount_path"].rstrip("/")
                data_dir = slot.get("data_dir", "").strip("/")
                output = f"{base}/{data_dir}" if data_dir else base
        except Exception:
            output = None
    output = output or OUTPUT_FALLBACK

    capture = start_capture(device_name, output=output, format=FORMAT_IMAGE)
    deadline = time.time() + float(timeout)
    final = dict(capture)
    while time.time() < deadline:
        time.sleep(_POLL_INTERVAL_S)
        status = get_capture_status(device_name)
        last = status["last_capture"]
        if last and last["id"] == capture["id"] and last["status"] in _TERMINAL:
            final = last
            break
    if final["status"] != "COMPLETED":
        raise RecameraError(f"Capture did not complete (status: {final['status']!r})")
    remote = f"{final['output_directory'].rstrip('/')}/{final['file_name']}"
    from .files import fetch_file

    blob = fetch_file(device_name, path=remote, raw=True)
    return {
        "event": final,
        "path": remote,
        "size": len(blob),
        "content_base64": base64.b64encode(blob).decode("ascii"),
    }


COMMANDS = {
    "get_capture_status": get_capture_status,
    "start_capture": start_capture,
    "stop_capture": stop_capture,
    "capture_image": capture_image,
}
COMMAND_SCHEMAS = {
    "get_capture_status": {"required": {"device_name"}, "optional": set()},
    "start_capture": {
        "required": {"device_name"},
        "optional": {"output", "format", "video_length_seconds"},
    },
    "stop_capture": {"required": {"device_name"}, "optional": set()},
    "capture_image": {"required": {"device_name"}, "optional": {"output", "timeout"}},
}
