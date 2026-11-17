#!/usr/bin/env python3
"""Preview and manage a gradual, consent-gated sleep schedule shift."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from sleep_core import (
    SleepRoutineError,
    default_data_dir,
    get_zone,
    hhmm_from_minutes,
    iso_now,
    load_json,
    load_profile,
    minutes_of_day,
    print_json,
    save_json,
    validate_date,
)

PLAN_FILE = "sleep-shift-plan.json"
ALLOWED_STEPS = {15, 30}


def plan_path(data_dir: Path) -> Path:
    return data_dir / PLAN_FILE


def signed_phase_delta(current: int, target: int, direction: str) -> int:
    clockwise = (target - current) % (24 * 60)
    if clockwise == 0:
        return 0
    if direction == "later":
        return clockwise
    if direction == "earlier":
        return clockwise - 24 * 60
    if clockwise == 12 * 60:
        raise SleepRoutineError("A 12-hour shift is ambiguous; choose --direction earlier or later")
    return clockwise if clockwise < 12 * 60 else clockwise - 24 * 60


def build_plan(args: argparse.Namespace, timezone: str) -> dict:
    get_zone(timezone)
    if args.step_minutes not in ALLOWED_STEPS:
        raise SleepRoutineError("--step-minutes must be 15 or 30")
    if not 1 <= args.hold_days <= 7:
        raise SleepRoutineError("--hold-days must be between 1 and 7")
    start_date = validate_date(args.start_date)
    current_sleep = minutes_of_day(args.current_sleep_time)
    target_sleep = minutes_of_day(args.target_sleep_time)
    if args.current_wake_time:
        minutes_of_day(args.current_wake_time)
    if args.target_wake_time:
        minutes_of_day(args.target_wake_time)
    delta = signed_phase_delta(current_sleep, target_sleep, args.direction)
    if delta == 0:
        raise SleepRoutineError("Current and target sleep times are already the same")

    sign = 1 if delta > 0 else -1
    remaining = abs(delta)
    stages = []
    cumulative = 0
    index = 1
    first_date = date.fromisoformat(start_date)
    while remaining:
        increment = min(args.step_minutes, remaining)
        cumulative += increment * sign
        stage_sleep = (current_sleep + cumulative) % (24 * 60)
        earliest = first_date + timedelta(days=(index - 1) * args.hold_days)
        stages.append(
            {
                "index": index,
                "sleep_time": hhmm_from_minutes(stage_sleep),
                "wind_down_at": hhmm_from_minutes(stage_sleep - args.wind_down_minutes),
                "shift_from_previous_minutes": increment * sign,
                "shift_from_baseline_minutes": cumulative,
                "earliest_start_date": earliest.isoformat(),
                "review_on_or_after": (earliest + timedelta(days=args.hold_days)).isoformat(),
            }
        )
        remaining -= increment
        index += 1

    return {
        "schema_version": 1,
        "timezone": timezone,
        "status": "preview",
        "direction": "later" if delta > 0 else "earlier",
        "current_sleep_time": args.current_sleep_time,
        "current_wake_time": args.current_wake_time,
        "target_sleep_time": args.target_sleep_time,
        "target_wake_time": args.target_wake_time,
        "wake_policy": "independent_optional",
        "sleep_duration_target_minutes": None,
        "phase_shift_minutes": delta,
        "step_minutes": args.step_minutes,
        "hold_days": args.hold_days,
        "wind_down_minutes": args.wind_down_minutes,
        "start_date": start_date,
        "estimated_minimum_days": len(stages) * args.hold_days,
        "current_stage_index": None,
        "stage_started_on": None,
        "review_on_or_after": None,
        "stages": stages,
        "created_at": None,
        "updated_at": None,
        "audit_history": [],
        "safety_note": (
            "This is a habit-support phase shift, not sleep restriction or medical treatment. "
            "It adjusts reminder timing without assuming a fixed sleep duration, and never auto-advances."
        ),
        "duration_note": (
            "Wake time and sleep duration are optional, variable observations. "
            "This plan does not grade or advance the user by duration."
        ),
    }


def update_profile_for_stage(data_dir: Path, plan: dict, stage: dict, action: str) -> None:
    profile = load_profile(data_dir)
    if profile.get("storage_consent") is not True:
        raise SleepRoutineError("An active local-storage consent is required")
    stamp = iso_now()
    old_sleep = profile.get("sleep_window_start")
    profile["sleep_window_start"] = stage["sleep_time"]
    profile["updated_at"] = stamp
    profile.setdefault("audit_history", []).append(
        {
            "at": stamp,
            "action": action,
            "old_sleep_window_start": old_sleep,
            "new_sleep_window_start": stage["sleep_time"],
            "wake_time_unchanged": True,
        }
    )
    save_json(data_dir / "profile.json", profile)


def current_stage(plan: dict) -> dict:
    index = plan.get("current_stage_index")
    if not isinstance(index, int) or index < 1 or index > len(plan.get("stages", [])):
        raise SleepRoutineError("Sleep-shift plan has no valid current stage")
    return plan["stages"][index - 1]


def audit_plan(plan: dict, action: str, **details) -> None:
    stamp = iso_now()
    plan["updated_at"] = stamp
    plan.setdefault("audit_history", []).append({"at": stamp, "action": action, **details})


def current_view(plan: dict, as_of: str) -> dict:
    stage = current_stage(plan)
    as_of_date = date.fromisoformat(validate_date(as_of))
    review_date = date.fromisoformat(plan["review_on_or_after"])
    return {
        "status": plan["status"],
        "timezone": plan["timezone"],
        "current_stage": stage,
        "target_sleep_time": plan["target_sleep_time"],
        "target_wake_time": plan["target_wake_time"],
        "review_due": plan["status"] == "active" and as_of_date >= review_date,
        "review_on_or_after": plan["review_on_or_after"],
        "remaining_stages": len(plan["stages"]) - stage["index"],
        "auto_advance": False,
        "measurement_note": (
            "Goodnight records preparation time, not actual sleep onset. Missing reports never count as success."
        ),
    }


def cmd_preview(args: argparse.Namespace) -> None:
    profile = load_profile(args.data_dir)
    timezone = args.timezone or profile.get("timezone")
    if not timezone:
        raise SleepRoutineError("Provide --timezone or initialize a profile first")
    output = build_plan(args, timezone)
    output["persisted"] = False
    print_json(output)


def cmd_start(args: argparse.Namespace) -> None:
    if not args.confirm:
        raise SleepRoutineError("Starting a sleep-shift plan requires --confirm")
    profile = load_profile(args.data_dir)
    if profile.get("storage_consent") is not True:
        raise SleepRoutineError("Save the profile with explicit consent before starting a plan")
    if profile.get("weekend_differs"):
        raise SleepRoutineError(
            "A gradual phase shift currently requires one consistent daily schedule. "
            "Align weekday and weekend settings before starting."
        )
    existing = load_json(plan_path(args.data_dir), {})
    if existing.get("status") in {"active", "paused"} and not args.replace:
        raise SleepRoutineError("An active or paused plan already exists; use --replace with explicit confirmation")
    timezone = args.timezone or profile.get("timezone")
    plan = build_plan(args, timezone)
    stamp = iso_now()
    first = plan["stages"][0]
    plan.update(
        {
            "status": "active",
            "current_stage_index": 1,
            "stage_started_on": plan["start_date"],
            "review_on_or_after": (
                date.fromisoformat(plan["start_date"]) + timedelta(days=plan["hold_days"])
            ).isoformat(),
            "created_at": stamp,
            "updated_at": stamp,
            "audit_history": [{"at": stamp, "action": "plan_started", "stage": 1}],
        }
    )
    update_profile_for_stage(args.data_dir, plan, first, "sleep_shift_started")
    save_json(plan_path(args.data_dir), plan)
    print_json({"started": True, "plan": plan, "current": current_view(plan, plan["start_date"])})


def cmd_show(args: argparse.Namespace) -> None:
    plan = load_json(plan_path(args.data_dir), {})
    if not plan:
        raise SleepRoutineError("No sleep-shift plan exists")
    print_json(plan)


def cmd_current(args: argparse.Namespace) -> None:
    plan = load_json(plan_path(args.data_dir), {})
    if not plan:
        raise SleepRoutineError("No sleep-shift plan exists")
    print_json(current_view(plan, args.as_of))


def cmd_advance(args: argparse.Namespace) -> None:
    if not args.confirm:
        raise SleepRoutineError("Advancing a sleep-shift stage requires --confirm")
    plan = load_json(plan_path(args.data_dir), {})
    if plan.get("status") != "active":
        raise SleepRoutineError("Only an active plan can advance")
    view = current_view(plan, args.as_of)
    if not view["review_due"]:
        raise SleepRoutineError(f"Hold this stage until at least {plan['review_on_or_after']}")
    current = current_stage(plan)
    if current["index"] == len(plan["stages"]):
        plan["status"] = "completed"
        audit_plan(plan, "plan_completed", stage=current["index"])
        save_json(plan_path(args.data_dir), plan)
        print_json({"completed": True, "plan": plan})
        return
    next_index = current["index"] + 1
    next_stage = plan["stages"][next_index - 1]
    plan["current_stage_index"] = next_index
    plan["stage_started_on"] = validate_date(args.as_of)
    plan["review_on_or_after"] = (
        date.fromisoformat(plan["stage_started_on"]) + timedelta(days=plan["hold_days"])
    ).isoformat()
    audit_plan(plan, "stage_advanced", old_stage=current["index"], new_stage=next_index)
    update_profile_for_stage(args.data_dir, plan, next_stage, "sleep_shift_advanced")
    save_json(plan_path(args.data_dir), plan)
    print_json({"advanced": True, "plan": plan, "current": current_view(plan, args.as_of)})


def cmd_hold(args: argparse.Namespace) -> None:
    plan = load_json(plan_path(args.data_dir), {})
    if plan.get("status") != "active":
        raise SleepRoutineError("Only an active plan can be held")
    if not 1 <= args.days <= 14:
        raise SleepRoutineError("--days must be between 1 and 14")
    base = max(date.fromisoformat(validate_date(args.as_of)), date.fromisoformat(plan["review_on_or_after"]))
    plan["review_on_or_after"] = (base + timedelta(days=args.days)).isoformat()
    audit_plan(plan, "stage_held", days=args.days, review_on_or_after=plan["review_on_or_after"])
    save_json(plan_path(args.data_dir), plan)
    print_json({"held": True, "plan": plan, "current": current_view(plan, args.as_of)})


def cmd_back(args: argparse.Namespace) -> None:
    if not args.confirm:
        raise SleepRoutineError("Moving back a stage requires --confirm")
    plan = load_json(plan_path(args.data_dir), {})
    if plan.get("status") not in {"active", "completed"}:
        raise SleepRoutineError("Only an active or completed plan can move back")
    current = current_stage(plan)
    if current["index"] == 1:
        raise SleepRoutineError("The plan is already at its first stage")
    previous_index = current["index"] - 1
    previous = plan["stages"][previous_index - 1]
    plan["status"] = "active"
    plan["current_stage_index"] = previous_index
    plan["stage_started_on"] = validate_date(args.as_of)
    plan["review_on_or_after"] = (
        date.fromisoformat(plan["stage_started_on"]) + timedelta(days=plan["hold_days"])
    ).isoformat()
    audit_plan(plan, "stage_moved_back", old_stage=current["index"], new_stage=previous_index)
    update_profile_for_stage(args.data_dir, plan, previous, "sleep_shift_moved_back")
    save_json(plan_path(args.data_dir), plan)
    print_json({"moved_back": True, "plan": plan, "current": current_view(plan, args.as_of)})


def cmd_pause(args: argparse.Namespace) -> None:
    plan = load_json(plan_path(args.data_dir), {})
    if plan.get("status") != "active":
        raise SleepRoutineError("Only an active plan can be paused")
    plan["status"] = "paused"
    audit_plan(plan, "plan_paused")
    save_json(plan_path(args.data_dir), plan)
    print_json({"paused": True, "plan": plan})


def cmd_resume(args: argparse.Namespace) -> None:
    plan = load_json(plan_path(args.data_dir), {})
    if plan.get("status") != "paused":
        raise SleepRoutineError("Only a paused plan can be resumed")
    plan["status"] = "active"
    plan["stage_started_on"] = validate_date(args.as_of)
    plan["review_on_or_after"] = (
        date.fromisoformat(plan["stage_started_on"]) + timedelta(days=plan["hold_days"])
    ).isoformat()
    audit_plan(plan, "plan_resumed", review_on_or_after=plan["review_on_or_after"])
    save_json(plan_path(args.data_dir), plan)
    print_json({"resumed": True, "plan": plan, "current": current_view(plan, args.as_of)})


def cmd_cancel(args: argparse.Namespace) -> None:
    if not args.confirm:
        raise SleepRoutineError("Cancelling a sleep-shift plan requires --confirm")
    plan = load_json(plan_path(args.data_dir), {})
    if not plan:
        raise SleepRoutineError("No sleep-shift plan exists")
    plan["status"] = "cancelled"
    audit_plan(plan, "plan_cancelled")
    save_json(plan_path(args.data_dir), plan)
    print_json({"cancelled": True, "plan": plan})


def add_plan_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--timezone")
    parser.add_argument("--current-sleep-time", required=True)
    parser.add_argument("--current-wake-time")
    parser.add_argument("--target-sleep-time", required=True)
    parser.add_argument("--target-wake-time")
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--direction", choices=["shortest", "earlier", "later"], default="shortest")
    parser.add_argument("--step-minutes", type=int, choices=sorted(ALLOWED_STEPS), default=15)
    parser.add_argument("--hold-days", type=int, default=2)
    parser.add_argument("--wind-down-minutes", type=int, choices=[30, 45, 60, 90], default=60)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    sub = parser.add_subparsers(dest="command", required=True)
    preview = sub.add_parser("preview")
    add_plan_arguments(preview)
    preview.set_defaults(func=cmd_preview)
    start = sub.add_parser("start")
    add_plan_arguments(start)
    start.add_argument("--confirm", action="store_true")
    start.add_argument("--replace", action="store_true")
    start.set_defaults(func=cmd_start)
    show = sub.add_parser("show")
    show.set_defaults(func=cmd_show)
    current = sub.add_parser("current")
    current.add_argument("--as-of", required=True)
    current.set_defaults(func=cmd_current)
    advance = sub.add_parser("advance")
    advance.add_argument("--as-of", required=True)
    advance.add_argument("--confirm", action="store_true")
    advance.set_defaults(func=cmd_advance)
    hold = sub.add_parser("hold")
    hold.add_argument("--as-of", required=True)
    hold.add_argument("--days", type=int, default=2)
    hold.set_defaults(func=cmd_hold)
    back = sub.add_parser("back")
    back.add_argument("--as-of", required=True)
    back.add_argument("--confirm", action="store_true")
    back.set_defaults(func=cmd_back)
    pause = sub.add_parser("pause")
    pause.set_defaults(func=cmd_pause)
    resume = sub.add_parser("resume")
    resume.add_argument("--as-of", required=True)
    resume.set_defaults(func=cmd_resume)
    cancel = sub.add_parser("cancel")
    cancel.add_argument("--confirm", action="store_true")
    cancel.set_defaults(func=cmd_cancel)
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
