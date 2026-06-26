#!/usr/bin/env python3
"""
Bridge OpenClaw Heartbeat runs to the proactive policy used by say-hi-to-me.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict

from proactive_scheduler import LOCAL_TZ, evaluate, mark_sent

ACK_TEXT = "HEARTBEAT_OK"


def parse_now(value: str | None) -> dt.datetime:
    if not value:
        return dt.datetime.now(tz=LOCAL_TZ)
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=LOCAL_TZ)
    return parsed.astimezone(LOCAL_TZ)


def build_heartbeat_response(
    skill_root: Path,
    now: dt.datetime,
    mark_delivered: bool = False,
) -> Dict[str, Any]:
    result = evaluate(skill_root, now)
    response_text = result.get("candidate_message") if result.get("eligible") else ACK_TEXT
    marked_sent = False

    if mark_delivered and result.get("eligible"):
        mark_sent(skill_root, now)
        marked_sent = True

    return {
        "checked_at": now.isoformat(timespec="seconds"),
        "eligible": result.get("eligible", False),
        "reason": result.get("reason", "unknown"),
        "candidate_message": result.get("candidate_message"),
        "next_eligible_at": result.get("next_eligible_at"),
        "response_text": response_text,
        "marked_sent": marked_sent,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Heartbeat bridge for say-hi-to-me")
    parser.add_argument("--skill-root", help="Skill root path, default script parent")
    parser.add_argument("--now", help="ISO datetime for deterministic checks")
    parser.add_argument("--mark-sent", action="store_true", help="Mark a successful heartbeat send in session state")
    parser.add_argument("--json", action="store_true", help="Print full JSON payload")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.skill_root).resolve() if args.skill_root else Path(__file__).resolve().parents[1]
    now = parse_now(args.now)
    payload = build_heartbeat_response(root, now, mark_delivered=args.mark_sent)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["response_text"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
