#!/usr/bin/env python3
"""Build reminder plans and state; never create Cron jobs or send messages."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from sleep_core import (
    SleepRoutineError,
    default_data_dir,
    hhmm_from_minutes,
    iso_now,
    load_json,
    load_profile,
    load_records,
    minutes_of_day,
    normalize_timestamp,
    parse_timestamp,
    print_json,
    save_json,
    time_is_allowed,
)

REMINDERS = {
    "wind_down": (
        "睡前准备",
        -60,
        "离你计划睡觉的时间还有一会儿，可以开始收尾、把节奏放慢了。完成 · 推迟 · 跳过 · 关闭此提醒",
    ),
    "hydration_wrap": (
        "晚间大量饮水收尾",
        -90,
        "如果你容易起夜，可以把大量饮水留在更早些时候；口渴仍可小口喝水。完成 · 推迟 · 跳过 · 关闭此提醒",
    ),
    "goodnight_invite": (
        "晚安邀请",
        0,
        "准备睡觉时跟我说一声晚安就好，我会记录时间，然后保持安静。",
    ),
    "sleep_time": (
        "阶段睡眠时间",
        0,
        "到了本阶段计划的睡眠时间。如果你准备好了，可以开始睡觉；还不困也不必勉强。"
        "想记录时对我说晚安就好。完成 · 推迟 · 跳过 · 关闭此提醒",
    ),
    "wake_target": ("目标起床", 0, "早上好。按你的设置，这是目标起床时间。完成 · 推迟 · 跳过 · 关闭此提醒"),
    "morning_checkin": ("晨间快速记录", 15, "醒来后跟我说声早安就好。跳过 · 关闭此提醒"),
    "weekly_summary": ("每周睡眠习惯摘要", 0, "生成一份只含描述性趋势的本周睡眠习惯摘要。"),
}

SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


def state_path(data_dir: Path) -> Path:
    return data_dir / "reminders.json"


def load_state(data_dir: Path) -> dict:
    return load_json(state_path(data_dir), {"schema_version": 1, "reminders": {}})


def reminder_state(state: dict, kind: str) -> dict:
    return state.setdefault("reminders", {}).setdefault(
        kind,
        {
            "enabled": True,
            "frequency": "daily",
            "ignored_streak": 0,
            "last_sent_at": None,
            "awaiting_reply": False,
            "snooze_until": None,
            "skipped_dates": [],
        },
    )


def adjusted_frequency(streak: int) -> str:
    if streak >= 6:
        return "weekly"
    if streak >= 3:
        return "every_other_day"
    return "daily"


def cmd_action(args: argparse.Namespace) -> None:
    if args.kind not in REMINDERS:
        raise SleepRoutineError(f"Unknown reminder: {args.kind}")
    profile = load_profile(args.data_dir)
    if profile.get("storage_consent") is not True:
        raise SleepRoutineError("Reminder preference storage requires local storage consent")
    state = load_state(args.data_dir)
    item = reminder_state(state, args.kind)
    stamp = normalize_timestamp(args.at, profile["timezone"]) if args.at else iso_now()
    today = parse_timestamp(stamp).date().isoformat()
    result = {"kind": args.kind, "action": args.action}
    if args.action == "sent":
        item["last_sent_at"] = stamp
        item["awaiting_reply"] = True
    elif args.action == "done":
        item.update({"awaiting_reply": False, "ignored_streak": 0, "frequency": "daily", "snooze_until": None})
    elif args.action == "postpone":
        if args.minutes <= 0:
            raise SleepRoutineError("--minutes must be positive")
        item["snooze_until"] = (
            parse_timestamp(stamp) + timedelta(minutes=args.minutes)
        ).isoformat(timespec="seconds")
        item["awaiting_reply"] = False
        result["snooze_until"] = item["snooze_until"]
    elif args.action == "skip":
        if today not in item["skipped_dates"]:
            item["skipped_dates"].append(today)
        item["awaiting_reply"] = False
    elif args.action == "disable":
        item["enabled"] = False
        item["awaiting_reply"] = False
    elif args.action == "ignored":
        item["ignored_streak"] += 1
        item["awaiting_reply"] = False
        item["frequency"] = adjusted_frequency(item["ignored_streak"])
        result["ask_adjustment"] = item["ignored_streak"] in {3, 6}
    elif args.action == "reduce":
        item["frequency"] = {
            "daily": "every_other_day",
            "every_other_day": "weekly",
            "weekly": "weekly",
        }[item["frequency"]]
        item["awaiting_reply"] = False
    state["updated_at"] = iso_now()
    save_json(state_path(args.data_dir), state)
    result["state"] = item
    print_json(result)


def load_shift_context(data_dir: Path) -> dict | None:
    plan = load_json(data_dir / "sleep-shift-plan.json", {})
    if plan.get("status") not in {"active", "paused"}:
        return None
    index = plan.get("current_stage_index")
    stages = plan.get("stages", [])
    if not isinstance(index, int) or index < 1 or index > len(stages):
        raise SleepRoutineError("Sleep-shift plan has no valid current stage")
    stage = stages[index - 1]
    return {
        "status": plan["status"],
        "direction": plan["direction"],
        "step_minutes": plan["step_minutes"],
        "hold_days": plan["hold_days"],
        "current_stage": stage,
        "target_sleep_time": plan["target_sleep_time"],
        "target_wake_time": plan.get("target_wake_time"),
        "review_on_or_after": plan["review_on_or_after"],
        "requires_schedule_refresh_after_stage_change": True,
    }


def schedule_items(
    profile: dict,
    shift: dict | None = None,
    enabled_override: set[str] | None = None,
) -> list[dict]:
    allowed_start = profile["proactive_start"]
    allowed_end = profile["proactive_end"]
    enabled = (
        enabled_override
        if enabled_override is not None
        else set(profile.get("enabled_reminders", []))
    )
    if shift:
        stage = shift["current_stage"]
        wake_value = stage.get("wake_time") or profile.get("target_wake_time")
        day_sets = [
            (
                "daily",
                minutes_of_day(stage["sleep_time"]),
                minutes_of_day(wake_value) if wake_value else None,
                "* * *",
            )
        ]
    else:
        wake_value = profile.get("target_wake_time")
        day_sets = [
            (
                "daily",
                minutes_of_day(profile["sleep_window_start"]),
                minutes_of_day(wake_value) if wake_value else None,
                "* * *",
            )
        ]
    if profile.get("weekend_differs") and not shift:
        required = ["weekend_sleep_window_start"]
        missing = [field for field in required if not profile.get(field)]
        if missing:
            raise SleepRoutineError("Missing weekend fields: " + ", ".join(missing))
        day_sets = [
            (
                "weekday",
                minutes_of_day(profile["sleep_window_start"]),
                minutes_of_day(profile["target_wake_time"])
                if profile.get("target_wake_time")
                else None,
                "* * 1-5",
            ),
            (
                "weekend",
                minutes_of_day(profile["weekend_sleep_window_start"]),
                minutes_of_day(profile["weekend_wake_time"])
                if profile.get("weekend_wake_time")
                else None,
                "* * 0,6",
            ),
        ]
    specs = []
    for variant, sleep_start, wake, days in day_sets:
        wind_down_minute = (
            minutes_of_day(shift["current_stage"]["wind_down_at"]) if shift else sleep_start - 60
        )
        specs.append(("wind_down", variant, wind_down_minute, days))
        bedtime_kind = "sleep_time" if "sleep_time" in enabled else "goodnight_invite"
        specs.append((bedtime_kind, variant, sleep_start, days))
        if wake is not None:
            specs.extend(
                [
                    ("wake_target", variant, wake, days),
                    ("morning_checkin", variant, wake + 15, days),
                ]
            )
        if profile.get("hydration_reminder_enabled"):
            specs.append(("hydration_wrap", variant, sleep_start - 90, days))
    summary_reference = (
        shift["current_stage"].get("wake_time") if shift else None
    ) or profile.get("weekend_wake_time") or profile.get("target_wake_time")
    summary_wake = minutes_of_day(summary_reference) if summary_reference else 12 * 60
    specs.append(("weekly_summary", "weekly", summary_wake + 30, "* * 0"))
    specs = [spec for spec in specs if spec[0] in enabled]
    items = []
    for kind, variant, minute, days in specs:
        at = hhmm_from_minutes(minute)
        allowed = time_is_allowed(at, allowed_start, allowed_end)
        label, _, message = REMINDERS[kind]
        items.append(
            {
                "kind": kind,
                "schedule_id": f"{kind}_{variant}",
                "label": label,
                "local_time": at,
                "allowed_by_proactive_window": allowed,
                "cron": f"{int(at[3:]):d} {int(at[:2]):d} {days}",
                "message": message,
            }
        )
    return items


def validated_identifier(value: str, field: str) -> str:
    if not SAFE_IDENTIFIER.fullmatch(value):
        raise SleepRoutineError(
            f"{field} must contain only letters, digits, dot, underscore, colon, or hyphen"
        )
    return value


def validated_target(value: str) -> str:
    if not value or len(value) > 256 or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise SleepRoutineError("delivery_target must be 1-256 printable characters without controls")
    return value


def scheduler_request_for(item: dict, profile: dict, agent: str) -> dict | None:
    if not item["allowed_by_proactive_window"]:
        return None
    validated_agent = validated_identifier(agent, "agent")
    validated_channel = validated_identifier(profile["delivery_channel"], "delivery_channel")
    target = validated_target(profile["delivery_target"])
    prompt = (
        f"Use $sleep-routine-coach for reminder type {item['kind']}. "
        "Run build_reminder_schedule.py evaluate with the current offset-aware time. "
        "If send is false, reply only NO_REPLY. If ask_adjustment is true, append a brief choice to reduce or disable it. "
        "If send is true, run action sent, then output exactly this gentle reminder: "
        f"{item['message']}"
    )
    argv = [
        "cron",
        "create",
        item["cron"],
        prompt,
        "--name",
        f"sleep-routine-coach:{item['schedule_id']}",
        "--declaration-key",
        f"sleep-routine-coach:{item['schedule_id']}",
        "--agent",
        validated_agent,
        "--session",
        "isolated",
        "--light-context",
        "--tz",
        profile["timezone"],
        "--announce",
        "--channel",
        validated_channel,
        "--to",
        target,
    ]
    return {
        "operation": "openclaw.cron.create",
        "executable": "openclaw",
        "argv": argv,
        "schedule_id": item["schedule_id"],
        "validated": True,
        "execution_policy": "Pass executable and argv separately; shell must be disabled.",
    }


def cmd_plan(args: argparse.Namespace) -> None:
    profile = load_profile(args.data_dir)
    required = [
        "timezone",
        "sleep_window_start",
        "proactive_start",
        "proactive_end",
    ]
    missing = [field for field in required if not profile.get(field)]
    if missing:
        raise SleepRoutineError("Missing profile fields: " + ", ".join(missing))
    shift = load_shift_context(args.data_dir)
    proposed = set(args.reminder) if args.reminder else None
    items = schedule_items(profile, shift, proposed)
    authorized = (
        profile.get("scheduling_consent") is True
        and bool(profile.get("delivery_channel"))
        and bool(profile.get("delivery_target"))
    )
    output = {
        "authorized": authorized,
        "created_jobs": [],
        "note": "Preview only. This script never executes OpenClaw or creates background jobs.",
        "sleep_shift": shift,
        "proposal_reminders": sorted(proposed) if proposed is not None else None,
        "items": items,
        "scheduler_requests": [
            scheduler_request_for(item, profile, args.agent) for item in items
        ]
        if authorized
        else [],
    }
    output["scheduler_requests"] = [
        request for request in output["scheduler_requests"] if request
    ]
    print_json(output)


def cmd_register_job(args: argparse.Namespace) -> None:
    profile = load_profile(args.data_dir)
    if profile.get("storage_consent") is not True or profile.get("scheduling_consent") is not True:
        raise SleepRoutineError("Registering an external job requires active storage and scheduling consent")
    state = load_state(args.data_dir)
    state.setdefault("external_jobs", {})[args.schedule_id] = {
        "job_id": args.job_id,
        "registered_at": iso_now(),
    }
    state["updated_at"] = iso_now()
    save_json(state_path(args.data_dir), state)
    print_json({"registered": True, "schedule_id": args.schedule_id, "job_id": args.job_id})


def cmd_unregister_job(args: argparse.Namespace) -> None:
    state = load_state(args.data_dir)
    removed = state.setdefault("external_jobs", {}).pop(args.schedule_id, None)
    if removed is not None:
        state["updated_at"] = iso_now()
        save_json(state_path(args.data_dir), state)
    print_json({"unregistered": removed is not None, "schedule_id": args.schedule_id, "job": removed})


def cmd_list_jobs(args: argparse.Namespace) -> None:
    print_json(load_state(args.data_dir).get("external_jobs", {}))


def cmd_evaluate(args: argparse.Namespace) -> None:
    profile = load_profile(args.data_dir)
    state = load_state(args.data_dir)
    item = reminder_state(state, args.kind)
    now = normalize_timestamp(args.at, profile["timezone"])
    local = parse_timestamp(now)
    today = local.date().isoformat()
    send = True
    reasons = []
    ask_adjustment = False
    if item.get("awaiting_reply") and item.get("last_sent_at"):
        last_date = parse_timestamp(item["last_sent_at"]).date().isoformat()
        if last_date < today:
            item["awaiting_reply"] = False
            item["ignored_streak"] += 1
            item["frequency"] = adjusted_frequency(item["ignored_streak"])
            ask_adjustment = item["ignored_streak"] in {3, 6}
            state["updated_at"] = iso_now()
            save_json(state_path(args.data_dir), state)
    if profile.get("scheduling_consent") is not True or profile.get("collection_enabled") is False:
        send, reasons = False, ["scheduling_not_authorized"]
    elif not item["enabled"]:
        send, reasons = False, ["disabled"]
    elif item["awaiting_reply"]:
        send, reasons = False, ["already_sent_without_reply"]
    elif today in item["skipped_dates"]:
        send, reasons = False, ["skipped_today"]
    elif item.get("snooze_until") and parse_timestamp(now) < parse_timestamp(item["snooze_until"]):
        send, reasons = False, ["snoozed"]
    elif not time_is_allowed(local.strftime("%H:%M"), profile["proactive_start"], profile["proactive_end"]):
        send, reasons = False, ["outside_authorized_hours"]
    elif args.kind in {
        "wind_down",
        "hydration_wrap",
        "goodnight_invite",
        "sleep_time",
        "weekly_summary",
    } and any(
        record.get("goodnight_at") and not record.get("morning_at") for record in load_records(args.data_dir)
    ):
        send, reasons = False, ["night_quiet"]
    if send and item["frequency"] == "every_other_day":
        send = local.toordinal() % 2 == 0
        if not send:
            reasons.append("reduced_frequency")
    elif send and item["frequency"] == "weekly":
        send = local.weekday() == 6
        if not send:
            reasons.append("reduced_frequency")
    hard_blockers = {
        "scheduling_not_authorized",
        "disabled",
        "already_sent_without_reply",
        "skipped_today",
        "snoozed",
        "outside_authorized_hours",
        "night_quiet",
    }
    if ask_adjustment and not hard_blockers.intersection(reasons):
        send = True
        reasons = [reason for reason in reasons if reason != "reduced_frequency"]
    print_json(
        {
            "send": send,
            "reasons": reasons,
            "kind": args.kind,
            "ask_adjustment": ask_adjustment,
            "state": item,
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--agent", default="main")
    plan.add_argument("--reminder", action="append", choices=sorted(REMINDERS))
    plan.set_defaults(func=cmd_plan)
    register = sub.add_parser("register-job")
    register.add_argument("--schedule-id", required=True)
    register.add_argument("--job-id", required=True)
    register.set_defaults(func=cmd_register_job)
    unregister = sub.add_parser("unregister-job")
    unregister.add_argument("--schedule-id", required=True)
    unregister.set_defaults(func=cmd_unregister_job)
    jobs = sub.add_parser("list-jobs")
    jobs.set_defaults(func=cmd_list_jobs)
    action = sub.add_parser("action")
    action.add_argument("kind", choices=sorted(REMINDERS))
    action.add_argument(
        "action",
        choices=["sent", "done", "postpone", "skip", "disable", "ignored", "reduce"],
    )
    action.add_argument("--minutes", type=int, default=20)
    action.add_argument("--at")
    action.set_defaults(func=cmd_action)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("kind", choices=sorted(REMINDERS))
    evaluate.add_argument("--at", required=True)
    evaluate.set_defaults(func=cmd_evaluate)
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
