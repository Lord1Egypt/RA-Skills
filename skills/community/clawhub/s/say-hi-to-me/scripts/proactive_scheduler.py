#!/usr/bin/env python3
"""
Proactive outreach scheduler for say-hi-to-me skill.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

LOCAL_TZ = dt.datetime.now().astimezone().tzinfo or dt.timezone.utc

INTERVAL_HOURS = {
    "low": 24,
    "mid": 12,
    "high": 6,
}


def parse_iso(ts: Optional[str]) -> Optional[dt.datetime]:
    if not ts:
        return None
    try:
        parsed = dt.datetime.fromisoformat(ts)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=LOCAL_TZ)
        return parsed.astimezone(LOCAL_TZ)
    except ValueError:
        return None


def parse_quiet_range(value: Optional[str]) -> Optional[Tuple[int, int]]:
    if not value:
        return None
    try:
        start_raw, end_raw = value.split("-", 1)
        sh, sm = [int(x) for x in start_raw.split(":")]
        eh, em = [int(x) for x in end_raw.split(":")]
        return sh * 60 + sm, eh * 60 + em
    except Exception:
        return None


def is_in_quiet_hours(now: dt.datetime, quiet: Optional[str]) -> bool:
    pair = parse_quiet_range(quiet)
    if not pair:
        return False
    start_m, end_m = pair
    current = now.hour * 60 + now.minute
    if start_m < end_m:
        return start_m <= current < end_m
    return current >= start_m or current < end_m


def next_quiet_end(now: dt.datetime, quiet: Optional[str]) -> Optional[str]:
    pair = parse_quiet_range(quiet)
    if not pair:
        return None
    start_m, end_m = pair
    today = now.date()

    end_today = dt.datetime.combine(today, dt.time(hour=end_m // 60, minute=end_m % 60), tzinfo=LOCAL_TZ)
    start_today = dt.datetime.combine(today, dt.time(hour=start_m // 60, minute=start_m % 60), tzinfo=LOCAL_TZ)

    if start_m < end_m:
        if now < start_today:
            return start_today.isoformat(timespec="seconds")
        if now < end_today:
            return end_today.isoformat(timespec="seconds")
        return (start_today + dt.timedelta(days=1)).isoformat(timespec="seconds")
    if now >= start_today:
        return (
            dt.datetime.combine(today + dt.timedelta(days=1), dt.time(hour=end_m // 60, minute=end_m % 60), tzinfo=LOCAL_TZ)
        ).isoformat(
            timespec="seconds"
        )
    return end_today.isoformat(timespec="seconds")


def read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def load_active_role_name(skill_root: Path, session: Dict[str, Any]) -> Optional[str]:
    active_rel = session.get("role", {}).get("active")
    if not active_rel:
        return None
    active_path = (skill_root / active_rel).resolve()
    role = read_yaml(active_path)
    return role.get("meta", {}).get("display_name")


def compose_message(now: dt.datetime, role_name: Optional[str], is_stale_context: bool) -> str:
    if 6 <= now.hour < 12:
        greet = "早安"
    elif 12 <= now.hour < 18:
        greet = "午安"
    elif 18 <= now.hour < 24:
        greet = "晚上好"
    else:
        greet = "你好"

    who = role_name or "我"
    if is_stale_context:
        return f"{greet}，{who}来打个招呼。你有空时再聊就好。"
    return f"{greet}，{who}在这儿。今天想先从哪件小事开始？"


def evaluate(skill_root: Path, now: dt.datetime) -> Dict[str, Any]:
    session_path = skill_root / "state" / "session.yaml"
    session = read_yaml(session_path)

    if not session:
        return {
            "eligible": False,
            "reason": "not_initialized",
            "candidate_message": None,
            "next_eligible_at": None,
        }

    proactive = session.get("proactive", {})
    enabled = proactive.get("enabled", False)
    if not enabled:
        return {
            "eligible": False,
            "reason": "proactive_disabled",
            "candidate_message": None,
            "next_eligible_at": None,
        }

    pause_until = parse_iso(proactive.get("pause_until"))
    if pause_until and now < pause_until:
        return {
            "eligible": False,
            "reason": "paused",
            "candidate_message": None,
            "next_eligible_at": pause_until.isoformat(timespec="seconds"),
        }

    quiet_hours = proactive.get("quiet_hours")
    if is_in_quiet_hours(now, quiet_hours):
        return {
            "eligible": False,
            "reason": "quiet_hours",
            "candidate_message": None,
            "next_eligible_at": next_quiet_end(now, quiet_hours),
        }

    freq = proactive.get("frequency", "mid")
    interval_hours = INTERVAL_HOURS.get(freq, INTERVAL_HOURS["mid"])
    last_sent = parse_iso(proactive.get("last_sent_at"))
    if last_sent:
        delta_h = (now - last_sent).total_seconds() / 3600
        if delta_h < interval_hours:
            next_time = last_sent + dt.timedelta(hours=interval_hours)
            return {
                "eligible": False,
                "reason": "cooldown",
                "candidate_message": None,
                "next_eligible_at": next_time.isoformat(timespec="seconds"),
            }

    freshness_hours = int(session.get("context", {}).get("freshness_hours", 72))
    last_user_input = parse_iso(session.get("last_user_input_at"))
    stale_context = True
    if last_user_input:
        stale_context = (now - last_user_input) > dt.timedelta(hours=freshness_hours)

    role_name = load_active_role_name(skill_root, session)
    message = compose_message(now=now, role_name=role_name, is_stale_context=stale_context)
    return {
        "eligible": True,
        "reason": "ok",
        "candidate_message": message,
        "next_eligible_at": None,
    }


def mark_sent(skill_root: Path, now: dt.datetime) -> None:
    session_path = skill_root / "state" / "session.yaml"
    session = read_yaml(session_path)
    if not session:
        return
    session.setdefault("proactive", {})
    session["proactive"]["last_sent_at"] = now.isoformat(timespec="seconds")
    session["updated_at"] = now.isoformat(timespec="seconds")
    write_yaml(session_path, session)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate proactive outreach schedule")
    parser.add_argument("--skill-root", help="Skill root path, default script parent")
    parser.add_argument("--now", help="ISO datetime for deterministic checks")
    parser.add_argument("--json", action="store_true", help="Print JSON result")
    parser.add_argument("--mark-sent", action="store_true", help="Mark proactive message as sent when eligible")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.skill_root).resolve() if args.skill_root else Path(__file__).resolve().parents[1]
    if args.now:
        parsed = dt.datetime.fromisoformat(args.now)
        now = parsed.replace(tzinfo=LOCAL_TZ) if parsed.tzinfo is None else parsed.astimezone(LOCAL_TZ)
    else:
        now = dt.datetime.now(tz=LOCAL_TZ)
    result = evaluate(root, now)
    result["checked_at"] = now.isoformat(timespec="seconds")

    if args.mark_sent and result.get("eligible"):
        mark_sent(root, now)
        result["marked_sent"] = True
    else:
        result["marked_sent"] = False

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["candidate_message"] or f"[skip] {result['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
