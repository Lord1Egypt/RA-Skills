"""High-level detection facade: schedule + rules + events (wraps ``rule`` and ``files``)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from . import rule as _rule
from . import files as _files
from . import storage as _storage

__all__ = [
    "get_detection_schedule",
    "set_detection_schedule",
    "get_detection_rules",
    "set_detection_rules",
    "get_detection_events",
    "clear_detection_events",
]


def get_detection_schedule(device_name: str) -> Optional[List[Dict[str, str]]]:
    """Alias for :func:`rule.get_schedule_rule`."""
    return _rule.get_schedule_rule(device_name)


def set_detection_schedule(
    device_name: str,
    schedule: Optional[List[Dict[str, str]]] = None,
) -> None:
    """Alias for :func:`rule.set_schedule_rule`.

    ``schedule`` defaults to ``None`` (meaning "always active"), so omitting
    the key from the CLI payload is equivalent to passing ``schedule: []``
    or ``schedule: null`` and clears any existing window.
    """
    _rule.set_schedule_rule(device_name, schedule)


def get_detection_rules(device_name: str) -> List[Dict[str, Any]]:
    """Active INFERENCE_SET rules, or ``[]`` when the trigger is not INFERENCE_SET."""
    trigger = _rule.get_record_trigger(device_name)
    if trigger["kind"] != "inference_set":
        return []
    return list(trigger["rules"])


def set_detection_rules(
    device_name: str,
    rules: List[Dict[str, Any]],
    *,
    ensure_writer: bool = True,
    ensure_storage: bool = True,
) -> None:
    """Install an INFERENCE_SET trigger with *rules*.

    Also (by default):
      * enables the rule pipeline with JPG writer (``ensure_writer=True``);
      * ensures a storage slot is available (``ensure_storage=True``).
    """
    if not isinstance(rules, list):
        raise ValueError("'rules' must be a list of detection-rule dicts.")
    if ensure_storage:
        _storage.ensure_storage(device_name)
    trigger = {"kind": "inference_set", "rules": rules}
    _rule.set_record_trigger(device_name, trigger)
    if ensure_writer:
        cfg = _rule.get_record_config(device_name)
        needs_update = (
            not cfg["rule_enabled"] or cfg["writer"].get("format", "").upper() != "JPG"
        )
        if needs_update:
            _rule.set_record_config(
                device_name,
                rule_enabled=True,
                writer_format="JPG",
                writer_interval_ms=cfg["writer"].get("interval_ms", 0),
            )


def get_detection_events(
    device_name: str,
    *,
    start_unix_ms: Optional[int] = None,
    end_unix_ms: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Normalized detection events, shape-compatible with the MCP server.

    Each event is ``{timestamp, timestamp_unix_ms, rule_name, snapshot_path?}`` where
    ``timestamp`` is an ISO-8601 UTC string. Use :func:`files.get_intellisense_events`
    to access the raw daemon payloads instead.
    """
    raw = _files.get_intellisense_events(
        device_name, start_unix_ms=start_unix_ms, end_unix_ms=end_unix_ms
    )
    out: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        ts = item.get("timestamp")
        if not isinstance(ts, (int, float)):
            continue
        ts_ms = int(ts)
        rule_id = (
            (item.get("id") or "").strip() if isinstance(item.get("id"), str) else ""
        )
        rule_name = rule_id or str(item.get("type", ""))
        file_event = item.get("file_event")
        snapshot_path: Optional[str] = None
        if isinstance(file_event, dict):
            p = file_event.get("path")
            if isinstance(p, str) and p:
                snapshot_path = p
        event = {
            "timestamp": datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "timestamp_unix_ms": ts_ms,
            "rule_name": rule_name,
        }
        if snapshot_path is not None:
            event["snapshot_path"] = snapshot_path
        out.append(event)
    return out


def clear_detection_events(device_name: str) -> None:
    """Alias for :func:`files.clear_intellisense_events`."""
    _files.clear_intellisense_events(device_name)


COMMANDS = {
    "get_detection_schedule": get_detection_schedule,
    "set_detection_schedule": set_detection_schedule,
    "get_detection_rules": get_detection_rules,
    "set_detection_rules": set_detection_rules,
    "get_detection_events": get_detection_events,
    "clear_detection_events": clear_detection_events,
}
COMMAND_SCHEMAS = {
    "get_detection_schedule": {"required": {"device_name"}, "optional": set()},
    "set_detection_schedule": {"required": {"device_name"}, "optional": {"schedule"}},
    "get_detection_rules": {"required": {"device_name"}, "optional": set()},
    "set_detection_rules": {
        "required": {"device_name", "rules"},
        "optional": {"ensure_writer", "ensure_storage"},
    },
    "get_detection_events": {
        "required": {"device_name"},
        "optional": {"start_unix_ms", "end_unix_ms"},
    },
    "clear_detection_events": {"required": {"device_name"}, "optional": set()},
}
