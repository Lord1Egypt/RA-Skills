#!/usr/bin/env python3
"""Create and manage the local sleep-routine profile with explicit consent."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from sleep_core import (
    SleepRoutineError,
    default_data_dir,
    get_zone,
    hhmm_from_minutes,
    iso_now,
    load_profile,
    minutes_of_day,
    parse_hhmm,
    print_json,
    save_json,
)


PROFILE_FIELDS = {
    "timezone",
    "target_wake_time",
    "sleep_window_start",
    "sleep_window_end",
    "weekend_differs",
    "weekend_wake_time",
    "weekend_sleep_window_start",
    "weekend_sleep_window_end",
    "often_nocturia",
    "hydration_reminder_enabled",
    "reminder_intensity",
    "proactive_start",
    "proactive_end",
    "storage_consent",
    "scheduling_consent",
    "delivery_channel",
    "delivery_target",
    "collection_enabled",
}
REMINDER_TYPES = {
    "wind_down",
    "hydration_wrap",
    "goodnight_invite",
    "sleep_time",
    "wake_target",
    "morning_checkin",
    "weekly_summary",
}


def parse_bool(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"true", "yes", "1", "on"}:
        return True
    if lowered in {"false", "no", "0", "off"}:
        return False
    raise SleepRoutineError(f"Expected true or false, got: {value}")


def coerce(field: str, value: str):
    if field in {
        "weekend_differs",
        "often_nocturia",
        "hydration_reminder_enabled",
        "storage_consent",
        "scheduling_consent",
        "collection_enabled",
    }:
        return parse_bool(value)
    if field == "timezone":
        get_zone(value)
    if field.endswith("_time") or field.endswith("_start") or field.endswith("_end"):
        if value != "24:00":
            parse_hhmm(value)
    if field == "reminder_intensity" and value not in {"minimal", "gentle", "standard"}:
        raise SleepRoutineError("reminder_intensity must be minimal, gentle, or standard")
    return value


def cmd_init(args: argparse.Namespace) -> None:
    if not args.consent:
        print_json({"persisted": False, "reason": "storage consent declined"})
        return
    get_zone(args.timezone)
    parse_hhmm(args.sleep_window_start)
    for value in (args.target_wake_time, args.sleep_window_end):
        if value:
            parse_hhmm(value)
    if bool(args.proactive_start) != bool(args.proactive_end):
        raise SleepRoutineError("Provide both --proactive-start and --proactive-end, or neither")
    proactive_start = args.proactive_start or hhmm_from_minutes(
        minutes_of_day(args.sleep_window_start) - 90
    )
    proactive_end = args.proactive_end or hhmm_from_minutes(
        minutes_of_day(args.sleep_window_start) + 30
    )
    parse_hhmm(proactive_start)
    if proactive_end != "24:00":
        parse_hhmm(proactive_end)
    if args.weekend_differs:
        if not args.weekend_sleep_window_start:
            raise SleepRoutineError(
                "Weekend sleep-window start is required when weekend-differs is enabled"
            )
        for value in (
            args.weekend_wake_time,
            args.weekend_sleep_window_start,
            args.weekend_sleep_window_end,
        ):
            if value:
                parse_hhmm(value)
    if args.hydration_reminder_enabled and not args.often_nocturia:
        raise SleepRoutineError("Hydration wrap-up reminders require an active nocturia concern and explicit opt-in")
    stamp = iso_now()
    profile = {
        "schema_version": 1,
        "timezone": args.timezone,
        "target_wake_time": args.target_wake_time,
        "sleep_window_start": args.sleep_window_start,
        "sleep_window_end": args.sleep_window_end,
        "weekend_differs": args.weekend_differs,
        "weekend_wake_time": args.weekend_wake_time,
        "weekend_sleep_window_start": args.weekend_sleep_window_start,
        "weekend_sleep_window_end": args.weekend_sleep_window_end,
        "often_nocturia": args.often_nocturia,
        "hydration_reminder_enabled": args.hydration_reminder_enabled,
        "reminder_intensity": args.reminder_intensity,
        "proactive_start": proactive_start,
        "proactive_end": proactive_end,
        "storage_consent": True,
        "scheduling_consent": False,
        "delivery_channel": None,
        "delivery_target": None,
        "enabled_reminders": [],
        "collection_enabled": True,
        "created_at": stamp,
        "updated_at": stamp,
        "audit_history": [{"at": stamp, "action": "storage_consent_granted"}],
    }
    save_json(args.data_dir / "profile.json", profile)
    print_json(
        {
            "persisted": True,
            "profile": profile,
            "defaults_applied": {
                "reminder_intensity": args.reminder_intensity,
                "proactive_window": [proactive_start, proactive_end]
                if not args.proactive_start
                else None,
                "sleep_duration_target": None,
            },
        }
    )


def cmd_show(args: argparse.Namespace) -> None:
    print_json(load_profile(args.data_dir))


def cmd_set(args: argparse.Namespace) -> None:
    if args.field not in PROFILE_FIELDS:
        raise SleepRoutineError(f"Unsupported profile field: {args.field}")
    profile = load_profile(args.data_dir)
    if not profile:
        raise SleepRoutineError("No persisted profile exists")
    if args.field == "storage_consent" and parse_bool(args.value) is False:
        raise SleepRoutineError("Use stop-collection or delete-all instead of silently revoking storage consent")
    value = coerce(args.field, args.value)
    if args.field == "hydration_reminder_enabled" and value is True and not profile.get("often_nocturia"):
        raise SleepRoutineError("Enable often_nocturia before opting into the hydration reminder")
    if args.field == "often_nocturia" and value is False and profile.get("hydration_reminder_enabled"):
        raise SleepRoutineError("Disable the hydration reminder before clearing the nocturia concern")
    old = profile.get(args.field)
    profile[args.field] = value
    profile["updated_at"] = iso_now()
    profile.setdefault("audit_history", []).append(
        {"at": profile["updated_at"], "action": "profile_updated", "field": args.field, "old": old, "new": value}
    )
    save_json(args.data_dir / "profile.json", profile)
    print_json({"updated": args.field, "value": value})


def cmd_authorize_schedule(args: argparse.Namespace) -> None:
    profile = load_profile(args.data_dir)
    if profile.get("storage_consent") is not True:
        raise SleepRoutineError("Save the profile with explicit consent before authorizing schedules")
    if not args.confirm:
        raise SleepRoutineError("Schedule authorization requires --confirm")
    if "hydration_wrap" in args.reminder and not profile.get("hydration_reminder_enabled"):
        raise SleepRoutineError("Hydration reminder is not enabled in the consented profile")
    if {"wake_target", "morning_checkin"}.intersection(args.reminder) and not profile.get(
        "target_wake_time"
    ):
        raise SleepRoutineError(
            "Wake and morning reminders require an optional target_wake_time first"
        )
    profile["scheduling_consent"] = True
    profile["delivery_channel"] = args.channel
    profile["delivery_target"] = args.target
    profile["enabled_reminders"] = sorted(set(args.reminder))
    profile["updated_at"] = iso_now()
    schedule_snapshot = {
        "timezone": profile.get("timezone"),
        "target_wake_time": profile.get("target_wake_time"),
        "sleep_window_start": profile.get("sleep_window_start"),
        "weekend_differs": profile.get("weekend_differs"),
        "weekend_wake_time": profile.get("weekend_wake_time"),
        "weekend_sleep_window_start": profile.get("weekend_sleep_window_start"),
        "proactive_start": profile.get("proactive_start"),
        "proactive_end": profile.get("proactive_end"),
        "reminders": profile["enabled_reminders"],
    }
    profile.setdefault("audit_history", []).append(
        {
            "at": profile["updated_at"],
            "action": "schedule_authorized",
            "channel": args.channel,
            "target": args.target,
            "schedule_snapshot": schedule_snapshot,
        }
    )
    save_json(args.data_dir / "profile.json", profile)
    print_json(
        {
            "authorized": True,
            "channel": args.channel,
            "target": args.target,
            "reminders": profile["enabled_reminders"],
        }
    )


def cmd_stop(args: argparse.Namespace) -> None:
    profile = load_profile(args.data_dir)
    if not profile:
        print_json({"stopped": True, "persisted_profile": False})
        return
    profile["collection_enabled"] = False
    profile["scheduling_consent"] = False
    profile["updated_at"] = iso_now()
    profile.setdefault("audit_history", []).append({"at": profile["updated_at"], "action": "collection_stopped"})
    save_json(args.data_dir / "profile.json", profile)
    shift_path = args.data_dir / "sleep-shift-plan.json"
    shift = json.loads(shift_path.read_text(encoding="utf-8")) if shift_path.exists() else {}
    if shift.get("status") == "active":
        shift["status"] = "paused"
        shift["updated_at"] = iso_now()
        shift.setdefault("audit_history", []).append(
            {"at": shift["updated_at"], "action": "plan_paused_collection_stopped"}
        )
        save_json(shift_path, shift)
    print_json({"stopped": True, "note": "Disable/remove existing external Cron jobs separately"})


def cmd_export(args: argparse.Namespace) -> None:
    export = {
        "exported_at": iso_now(),
        "profile": load_profile(args.data_dir),
        "records": json.loads((args.data_dir / "sleep-records.json").read_text(encoding="utf-8"))
        if (args.data_dir / "sleep-records.json").exists()
        else [],
        "reminders": json.loads((args.data_dir / "reminders.json").read_text(encoding="utf-8"))
        if (args.data_dir / "reminders.json").exists()
        else {},
        "sleep_shift_plan": json.loads(
            (args.data_dir / "sleep-shift-plan.json").read_text(encoding="utf-8")
        )
        if (args.data_dir / "sleep-shift-plan.json").exists()
        else {},
    }
    if args.output:
        save_json(args.output, export)
        print_json({"exported": True, "path": str(args.output)})
    else:
        print_json(export)


def cmd_delete_all(args: argparse.Namespace) -> None:
    if not args.confirm:
        raise SleepRoutineError("Deletion requires --confirm")
    removed = []
    if args.data_dir.exists():
        for child in args.data_dir.iterdir():
            if child.is_file():
                child.unlink()
                removed.append(child.name)
            elif child.is_dir():
                shutil.rmtree(child)
                removed.append(child.name + "/")
        try:
            args.data_dir.rmdir()
        except OSError:
            pass
    print_json({"deleted": True, "removed": sorted(removed)})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--consent", action="store_true")
    init.add_argument("--timezone", required=True)
    init.add_argument("--target-wake-time")
    init.add_argument("--sleep-window-start", required=True)
    init.add_argument("--sleep-window-end")
    init.add_argument("--weekend-differs", action="store_true")
    init.add_argument("--weekend-wake-time")
    init.add_argument("--weekend-sleep-window-start")
    init.add_argument("--weekend-sleep-window-end")
    init.add_argument("--often-nocturia", action="store_true")
    init.add_argument("--hydration-reminder-enabled", action="store_true")
    init.add_argument("--reminder-intensity", choices=["minimal", "gentle", "standard"], default="gentle")
    init.add_argument("--proactive-start")
    init.add_argument("--proactive-end")
    init.set_defaults(func=cmd_init)

    show = sub.add_parser("show")
    show.set_defaults(func=cmd_show)

    set_cmd = sub.add_parser("set")
    set_cmd.add_argument("field")
    set_cmd.add_argument("value")
    set_cmd.set_defaults(func=cmd_set)

    authorize = sub.add_parser("authorize-schedule")
    authorize.add_argument("--confirm", action="store_true")
    authorize.add_argument("--channel", required=True)
    authorize.add_argument("--target", required=True)
    authorize.add_argument("--reminder", action="append", choices=sorted(REMINDER_TYPES), required=True)
    authorize.set_defaults(func=cmd_authorize_schedule)

    stop = sub.add_parser("stop-collection")
    stop.set_defaults(func=cmd_stop)

    export = sub.add_parser("export")
    export.add_argument("--output", type=Path)
    export.set_defaults(func=cmd_export)

    delete = sub.add_parser("delete-all")
    delete.add_argument("--confirm", action="store_true")
    delete.set_defaults(func=cmd_delete_all)
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
