"""High-level detection facade: schedule + rules + events (wraps ``rule`` and ``files``)."""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from . import files as _files
from . import rule as _rule
from . import storage as _storage
from ._coerce import to_bool

__all__ = [
    "get_detection_schedule",
    "set_detection_schedule",
    "get_detection_rules",
    "set_detection_rules",
    "get_detection_events",
    "clear_detection_events",
]


def get_detection_schedule(device_name: Optional[str] = None) -> Optional[List[Dict[str, str]]]:
    """Alias for :func:`rule.get_schedule_rule`."""
    return _rule.get_schedule_rule(device_name)


def set_detection_schedule(
    device_name: Optional[str] = None,
    schedule: Optional[List[Dict[str, str]]] = None,
) -> None:
    """Alias for :func:`rule.set_schedule_rule`.

    `schedule` defaults to `None` (meaning "always active"), so omitting
    the key from the CLI payload is equivalent to passing `schedule: []`
    or `schedule: null` and clears any existing window.
    """
    _rule.set_schedule_rule(device_name, schedule)


def get_detection_rules(device_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Active INFERENCE_SET rules, or `[]` when the trigger is not INFERENCE_SET
    (including a retired-but-unmigrated ``SED`` selection)."""
    return list(_rule._get_inference_rules(device_name))


DEFAULT_VISION_SOURCE = "builtin"


def _validate_rules_against_sources(
    rules: List[Dict[str, Any]], sources: List[Dict[str, Any]]
) -> None:
    """Fail loudly on unknown source ids or labels the selected sources can
    never produce — a silently never-firing rule is the worst outcome. The
    ``builtin`` source's classes follow the selected vision model (unknowable
    here), so its presence skips the label check: never cry wolf."""
    by_id = {s["id"]: s for s in sources}
    for rule in rules:
        name = rule.get("name", "")
        selected = list(rule.get("source_filter") or [])
        if not selected:  # explicit empty = all sources
            selected = list(by_id)
        unknown = [sid for sid in selected if sid not in by_id]
        if unknown:
            raise ValueError(
                f"rule {name!r}: unknown source_filter id(s) {unknown}; "
                f"available: {sorted(by_id)}"
            )
        labels = list(rule.get("label_filter") or [])
        if not labels:
            continue
        picked = [by_id[sid] for sid in selected]
        if any(s["kind"] == "builtin" for s in picked):
            continue  # builtin classes follow the active vision model: unknowable
        producible = {c for s in picked for c in s["classes"]}
        bad = [lbl for lbl in labels if lbl not in producible]
        if bad:
            states = ", ".join(
                f"{s['id']}({'running' if s['running'] else 'STOPPED'}, "
                f"{len(s['classes'])} classes)" for s in picked
            )
            raise ValueError(
                f"rule {name!r}: label(s) {bad} cannot be produced by the "
                f"selected source(s) [{states}]; check get_record_sources and "
                f"the AcousticsLab/App Center state before compiling this rule"
            )


def set_detection_rules(
    device_name: Optional[str] = None,
    *,
    rules: List[Dict[str, Any]],
    ensure_writer: bool = True,
    ensure_storage: bool = True,
) -> None:
    """Install an INFERENCE_SET trigger with *rules*.

    Rules without ``source_filter`` are scoped to the ``builtin`` vision
    source — an empty filter matches EVERY source, including acoustic
    classifications. Pass ``source_filter=[\"acousticslab\"]`` for sound.
    Source ids and labels are validated against ``get_record_sources`` first.

    Also (by default):
      * enables the rule pipeline with JPG writer (`ensure_writer=True`);
      * ensures a storage slot is available (`ensure_storage=True`).
    """
    if not isinstance(rules, list):
        raise ValueError("'rules' must be a list of detection-rule dicts.")
    ensure_writer = to_bool(ensure_writer, "ensure_writer")
    ensure_storage = to_bool(ensure_storage, "ensure_storage")
    prepared: List[Dict[str, Any]] = []
    for rule in rules:
        r = dict(rule)
        if r.get("source_filter") is None:
            r["source_filter"] = [DEFAULT_VISION_SOURCE]
        prepared.append(r)
    if prepared:
        _validate_rules_against_sources(prepared, _rule.get_record_sources(device_name))
    if ensure_storage:
        _storage.ensure_storage(device_name)
    trigger = {"kind": "inference_set", "rules": prepared}
    _rule.set_record_trigger(device_name, trigger=trigger)
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
    device_name: Optional[str] = None,
    *,
    start_unix_ms: Optional[int] = None,
    end_unix_ms: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Normalized detection events, shape-compatible with the MCP server.

    Each event is `{timestamp, timestamp_unix_ms, rule_name, snapshot_path?}` where
    `timestamp` is an ISO-8601 UTC string. Use :func:`files.get_intellisense_events`
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


def clear_detection_events(device_name: Optional[str] = None) -> None:
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
