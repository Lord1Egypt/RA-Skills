#!/usr/bin/env python3
"""Record, correct, view, export, and delete sleep events."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sleep_core import (
    SleepRoutineError,
    default_data_dir,
    elapsed_minutes,
    find_record,
    load_profile,
    load_records,
    local_date_for_goodnight,
    new_record,
    normalize_timestamp,
    now_in_zone,
    previous_local_date,
    print_json,
    public_record,
    recalculate_record,
    require_storage_consent,
    save_records,
    set_field,
    validate_date,
)


EDITABLE_FIELDS = {
    "goodnight_at",
    "reported_sleep_at",
    "sleep_latency_minutes",
    "sleep_latency_category",
    "morning_at",
    "out_of_bed_at",
    "night_awakenings",
    "night_awakenings_category",
    "night_awake_minutes",
    "nocturia_count",
    "nocturia_category",
    "rested_score",
    "notes",
}
TIMESTAMP_FIELDS = {"goodnight_at", "reported_sleep_at", "morning_at", "out_of_bed_at"}
INTEGER_FIELDS = {
    "sleep_latency_minutes",
    "night_awakenings",
    "night_awake_minutes",
    "nocturia_count",
    "rested_score",
}
CATEGORY_VALUES = {
    "sleep_latency_category": {"quick", "about_30", "over_60", "unknown"},
    "night_awakenings_category": {"3_plus", "unknown"},
    "nocturia_category": {"3_plus", "unknown"},
}


def context(args: argparse.Namespace):
    profile = load_profile(args.data_dir)
    zone_name = args.timezone or profile.get("timezone")
    if not zone_name:
        raise SleepRoutineError("Timezone is required in the profile or via --timezone")
    return profile, zone_name


def persist_or_ephemeral(profile, payload):
    if profile.get("storage_consent") is not True or profile.get("collection_enabled") is False:
        payload.update({"persisted": False, "reason": "storage consent or collection is not active"})
        print_json(payload)
        return False
    return True


def cmd_goodnight(args: argparse.Namespace) -> None:
    profile, zone_name = context(args)
    at = normalize_timestamp(args.at, zone_name) if args.at else now_in_zone(zone_name)
    session_date = validate_date(args.date) if args.date else local_date_for_goodnight(at, zone_name)
    if not persist_or_ephemeral(profile, {"event": "goodnight", "goodnight_at": at, "date": session_date}):
        return
    records = load_records(args.data_dir)
    record = find_record(records, session_date)
    if record is None:
        record = new_record(session_date, zone_name, args.source)
        records.append(record)
    set_field(
        record,
        "goodnight_at",
        at,
        source=args.source,
        action="goodnight_replaced" if record.get("goodnight_at") else "goodnight_recorded",
        reason=args.reason,
    )
    recalculate_record(record)
    save_records(args.data_dir, records)
    print_json({"persisted": True, "record": public_record(record)})


def cmd_morning(args: argparse.Namespace) -> None:
    profile, zone_name = context(args)
    at = normalize_timestamp(args.at, zone_name) if args.at else now_in_zone(zone_name)
    records = load_records(args.data_dir)
    open_records = [r for r in records if r.get("goodnight_at") and not r.get("morning_at")]
    fallback_date = previous_local_date(at, zone_name)
    session_date = validate_date(args.date) if args.date else (
        sorted(open_records, key=lambda r: r["date"])[-1]["date"] if open_records else fallback_date
    )
    if not persist_or_ephemeral(profile, {"event": "morning", "morning_at": at, "date": session_date}):
        return
    record = find_record(records, session_date)
    if record is None:
        record = new_record(session_date, zone_name, args.source)
        records.append(record)
    set_field(
        record,
        "morning_at",
        at,
        source=args.source,
        action="morning_replaced" if record.get("morning_at") else "morning_recorded",
        reason=args.reason,
    )
    recalculate_record(record)
    save_records(args.data_dir, records)
    print_json({"persisted": True, "record": public_record(record)})


def cmd_sleep_onset(args: argparse.Namespace) -> None:
    profile, zone_name = context(args)
    require_storage_consent(profile)
    if profile.get("collection_enabled") is False:
        raise SleepRoutineError("Collection is stopped")
    records = load_records(args.data_dir)
    record = find_record(records, validate_date(args.date))
    if record is None or not record.get("goodnight_at"):
        raise SleepRoutineError("A goodnight event is required before recording reported sleep onset")
    at = normalize_timestamp(args.at, zone_name)
    latency = elapsed_minutes(record["goodnight_at"], at)
    if latency < 0 or latency > 24 * 60:
        raise SleepRoutineError("Reported sleep onset must be between goodnight and 24 hours later")
    set_field(
        record,
        "reported_sleep_at",
        at,
        source=args.source,
        action="reported_sleep_onset",
        reason=args.reason,
    )
    set_field(
        record,
        "sleep_latency_minutes",
        latency,
        source="derived",
        action="latency_from_reported_sleep_onset",
        reason=args.reason,
    )
    recalculate_record(record)
    save_records(args.data_dir, records)
    print_json({"persisted": True, "record": public_record(record, include_audit=args.include_audit)})


def parse_value(field: str, raw: str, zone_name: str):
    if raw.lower() == "null":
        return None
    if field in TIMESTAMP_FIELDS:
        return normalize_timestamp(raw, zone_name)
    if field in INTEGER_FIELDS:
        try:
            value = int(raw)
        except ValueError as exc:
            raise SleepRoutineError(f"{field} must be an integer or null") from exc
        if value < 0:
            raise SleepRoutineError(f"{field} cannot be negative")
        if field == "rested_score" and value > 5:
            raise SleepRoutineError("rested_score must be from 0 to 5")
        return value
    if field in CATEGORY_VALUES and raw not in CATEGORY_VALUES[field]:
        raise SleepRoutineError(
            f"{field} must be one of: {', '.join(sorted(CATEGORY_VALUES[field]))}, or null"
        )
    return raw


def cmd_correct(args: argparse.Namespace) -> None:
    profile, zone_name = context(args)
    require_storage_consent(profile)
    if profile.get("collection_enabled") is False:
        raise SleepRoutineError("Collection is stopped")
    if args.field not in EDITABLE_FIELDS:
        raise SleepRoutineError(f"Unsupported field: {args.field}")
    records = load_records(args.data_dir)
    record = find_record(records, validate_date(args.date))
    if record is None:
        raise SleepRoutineError(f"No record for {args.date}")
    value = parse_value(args.field, args.value, zone_name)
    set_field(record, args.field, value, source=args.source, action="corrected", reason=args.reason)
    recalculate_record(record)
    save_records(args.data_dir, records)
    print_json({"corrected": True, "record": public_record(record, include_audit=args.include_audit)})


def cmd_cancel_goodnight(args: argparse.Namespace) -> None:
    args.field = "goodnight_at"
    args.value = "null"
    args.reason = args.reason or "User said the previous goodnight did not count"
    cmd_correct(args)


def cmd_show(args: argparse.Namespace) -> None:
    records = load_records(args.data_dir)
    if args.date:
        record = find_record(records, validate_date(args.date))
        print_json(public_record(record, args.include_audit) if record else {})
    else:
        print_json([public_record(record, args.include_audit) for record in records])


def cmd_delete(args: argparse.Namespace) -> None:
    profile = load_profile(args.data_dir)
    require_storage_consent(profile)
    session_date = validate_date(args.date)
    records = load_records(args.data_dir)
    remaining = [record for record in records if record.get("date") != session_date]
    deleted = len(records) - len(remaining)
    if deleted:
        save_records(args.data_dir, remaining)
    print_json({"deleted": bool(deleted), "date": session_date})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--timezone")
    sub = parser.add_subparsers(dest="command", required=True)

    for name, function in (("goodnight", cmd_goodnight), ("morning", cmd_morning)):
        command = sub.add_parser(name)
        command.add_argument("--at")
        command.add_argument("--date")
        command.add_argument("--source", default="user_report")
        command.add_argument("--reason")
        command.set_defaults(func=function)

    onset = sub.add_parser("sleep-onset")
    onset.add_argument("--date", required=True)
    onset.add_argument("--at", required=True)
    onset.add_argument("--source", default="user_report")
    onset.add_argument("--reason")
    onset.add_argument("--include-audit", action="store_true")
    onset.set_defaults(func=cmd_sleep_onset)

    correct = sub.add_parser("correct")
    correct.add_argument("--date", required=True)
    correct.add_argument("--field", required=True)
    correct.add_argument("--value", required=True)
    correct.add_argument("--source", default="user_correction")
    correct.add_argument("--reason")
    correct.add_argument("--include-audit", action="store_true")
    correct.set_defaults(func=cmd_correct)

    cancel = sub.add_parser("cancel-goodnight")
    cancel.add_argument("--date", required=True)
    cancel.add_argument("--source", default="user_correction")
    cancel.add_argument("--reason")
    cancel.add_argument("--include-audit", action="store_true")
    cancel.set_defaults(func=cmd_cancel_goodnight)

    show = sub.add_parser("show")
    show.add_argument("--date")
    show.add_argument("--include-audit", action="store_true")
    show.set_defaults(func=cmd_show)

    delete = sub.add_parser("delete")
    delete.add_argument("--date", required=True)
    delete.set_defaults(func=cmd_delete)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except (SleepRoutineError, json.JSONDecodeError, OSError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
