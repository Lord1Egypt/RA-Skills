#!/usr/bin/env python3
"""Shared, dependency-free storage and time helpers for sleep-routine-coach."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

APP_NAME = "sleep-routine-coach"
RECORD_FIELDS = [
    "date",
    "timezone",
    "goodnight_at",
    "sleep_latency_minutes",
    "estimated_sleep_at",
    "morning_at",
    "out_of_bed_at",
    "night_awakenings",
    "nocturia_count",
    "rested_score",
    "notes",
    "source",
    "created_at",
    "updated_at",
]


class SleepRoutineError(ValueError):
    """A user-actionable validation error."""


def default_data_dir() -> Path:
    override = os.environ.get("SLEEP_ROUTINE_DATA_DIR")
    if override:
        return Path(override).expanduser()
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / APP_NAME


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.chmod(0o700)
    except OSError:
        pass


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, value: Any) -> None:
    ensure_private_dir(path.parent)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.chmod(temp_name, 0o600)
        os.replace(temp_name, path)
        try:
            path.chmod(0o600)
        except OSError:
            pass
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat(timespec="seconds")


def get_zone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise SleepRoutineError(f"Unknown IANA timezone: {name}") from exc


def parse_timestamp(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise SleepRoutineError(f"Invalid ISO 8601 timestamp: {value}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise SleepRoutineError("Timestamp must include a UTC offset, for example 2026-07-29T23:06:00-04:00")
    return parsed


def normalize_timestamp(value: str, zone_name: str) -> str:
    parsed = parse_timestamp(value)
    return parsed.astimezone(get_zone(zone_name)).isoformat(timespec="seconds")


def now_in_zone(zone_name: str) -> str:
    return utc_now().astimezone(get_zone(zone_name)).isoformat(timespec="seconds")


def elapsed_minutes(start: str, end: str) -> int:
    start_dt = parse_timestamp(start).astimezone(timezone.utc)
    end_dt = parse_timestamp(end).astimezone(timezone.utc)
    return round((end_dt - start_dt).total_seconds() / 60)


def add_elapsed_minutes(value: str, minutes: int, zone_name: str) -> str:
    absolute = parse_timestamp(value).astimezone(timezone.utc) + timedelta(minutes=minutes)
    return absolute.astimezone(get_zone(zone_name)).isoformat(timespec="seconds")


def local_date_for_goodnight(timestamp: str, zone_name: str) -> str:
    return parse_timestamp(timestamp).astimezone(get_zone(zone_name)).date().isoformat()


def previous_local_date(timestamp: str, zone_name: str) -> str:
    local = parse_timestamp(timestamp).astimezone(get_zone(zone_name))
    return (local.date() - timedelta(days=1)).isoformat()


def parse_hhmm(value: str) -> time:
    try:
        parsed = time.fromisoformat(value)
    except ValueError as exc:
        raise SleepRoutineError(f"Invalid time: {value}; use HH:MM") from exc
    if parsed.second or parsed.microsecond:
        raise SleepRoutineError("Use minute precision (HH:MM)")
    return parsed


def minutes_of_day(value: str) -> int:
    parsed = parse_hhmm(value)
    return parsed.hour * 60 + parsed.minute


def hhmm_from_minutes(value: int) -> str:
    value %= 24 * 60
    return f"{value // 60:02d}:{value % 60:02d}"


def time_is_allowed(value: str, start: str, end: str) -> bool:
    candidate = minutes_of_day(value)
    low = minutes_of_day(start)
    high = 24 * 60 if end == "24:00" else minutes_of_day(end)
    if low < high:
        return low <= candidate < high
    if low > high:
        return candidate >= low or candidate < high
    return False


def load_profile(data_dir: Path) -> dict[str, Any]:
    return load_json(data_dir / "profile.json", {})


def load_records(data_dir: Path) -> list[dict[str, Any]]:
    return load_json(data_dir / "sleep-records.json", [])


def save_records(data_dir: Path, records: list[dict[str, Any]]) -> None:
    save_json(data_dir / "sleep-records.json", records)


def require_storage_consent(profile: dict[str, Any]) -> None:
    if profile.get("storage_consent") is not True:
        raise SleepRoutineError("Local storage consent is not active; no sleep data was written")


def find_record(records: list[dict[str, Any]], session_date: str) -> dict[str, Any] | None:
    return next((record for record in records if record.get("date") == session_date), None)


def new_record(session_date: str, zone_name: str, source: str) -> dict[str, Any]:
    stamp = iso_now()
    record = {field: None for field in RECORD_FIELDS}
    record.update(
        {
            "date": session_date,
            "timezone": zone_name,
            "source": source,
            "created_at": stamp,
            "updated_at": stamp,
            "night_awake_minutes": None,
            "reported_sleep_at": None,
            "sleep_latency_category": None,
            "night_awakenings_category": None,
            "nocturia_category": None,
            "estimated_sleep_duration_minutes": None,
            "reported_window_minutes": None,
            "provenance": {},
            "audit_history": [],
        }
    )
    return record


def audit(
    record: dict[str, Any],
    action: str,
    *,
    field: str | None = None,
    old: Any = None,
    new: Any = None,
    source: str = "user_report",
    reason: str | None = None,
) -> None:
    entry = {
        "at": iso_now(),
        "action": action,
        "field": field,
        "old": old,
        "new": new,
        "source": source,
        "reason": reason,
    }
    record.setdefault("audit_history", []).append(entry)
    record["updated_at"] = entry["at"]
    if field:
        record.setdefault("provenance", {})[field] = {
            "kind": "derived" if source == "derived" else ("estimated" if source == "estimated" else "reported"),
            "source": source,
            "updated_at": entry["at"],
        }


def set_field(
    record: dict[str, Any],
    field: str,
    value: Any,
    *,
    source: str,
    action: str = "set",
    reason: str | None = None,
) -> None:
    old = record.get(field)
    record[field] = value
    audit(record, action, field=field, old=old, new=value, source=source, reason=reason)


def recalculate_record(record: dict[str, Any]) -> dict[str, Any]:
    zone_name = record["timezone"]
    goodnight = record.get("goodnight_at")
    latency = record.get("sleep_latency_minutes")
    estimated_sleep = None
    if goodnight is not None and latency is not None:
        estimated_sleep = add_elapsed_minutes(goodnight, int(latency), zone_name)
    if record.get("estimated_sleep_at") != estimated_sleep:
        set_field(record, "estimated_sleep_at", estimated_sleep, source="estimated", action="recalculate")

    duration = None
    morning = record.get("morning_at")
    awake_minutes = record.get("night_awake_minutes")
    awakenings = record.get("night_awakenings")
    known_awake = awake_minutes is not None or awakenings == 0
    if estimated_sleep and morning and known_awake:
        total = elapsed_minutes(estimated_sleep, morning)
        awake = int(awake_minutes or 0)
        if total >= 0 and 0 <= awake <= total:
            duration = total - awake
    if record.get("estimated_sleep_duration_minutes") != duration:
        set_field(
            record,
            "estimated_sleep_duration_minutes",
            duration,
            source="estimated",
            action="recalculate",
        )
    window = elapsed_minutes(goodnight, morning) if goodnight and morning else None
    if window is not None and window < 0:
        window = None
    if record.get("reported_window_minutes") != window:
        set_field(record, "reported_window_minutes", window, source="derived", action="recalculate")
    return record


def validate_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise SleepRoutineError(f"Invalid date: {value}; use YYYY-MM-DD") from exc


def public_record(record: dict[str, Any], include_audit: bool = False) -> dict[str, Any]:
    result = dict(record)
    if not include_audit:
        result.pop("audit_history", None)
    return result


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))
