#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR / "replay"))

from replay_common import redact_text

DEFAULT_FEEDBACK_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-feedback.jsonl"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def record_feedback(args: argparse.Namespace) -> dict:
    feedback_file = Path(args.feedback_file).expanduser().resolve()
    feedback_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at": utc_now(),
        "skill": args.skill,
        "agent": redact_text(args.agent_name) if args.agent_name else None,
        "rating": args.rating,
        "feedback": redact_text(args.feedback.strip()),
        "task": redact_text(args.task.strip()) if args.task else None,
        "expected": redact_text(args.expected.strip()) if args.expected else None,
        "actual": redact_text(args.actual.strip()) if args.actual else None,
        "tags": [tag.strip() for tag in args.tags.split(",") if tag.strip()],
        "source": args.source,
        "privacy": "redacted",
    }
    line = json.dumps(payload, ensure_ascii=False) + "\n"
    with feedback_file.open("a", encoding="utf-8") as handle:
        try:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        except Exception:
            pass
        try:
            handle.write(line)
            handle.flush()
        finally:
            try:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass
    return {"recorded": True, "feedback_file": str(feedback_file), "entry": payload}


def main() -> int:
    parser = argparse.ArgumentParser(description="Record usage feedback for a generated or installed skill.")
    parser.add_argument("--skill", required=True, help="Skill name.")
    parser.add_argument("--feedback", required=True, help="User or agent feedback.")
    parser.add_argument("--agent-name", default="", help="Agent that used the skill.")
    parser.add_argument("--rating", choices=["positive", "neutral", "negative"], default="neutral")
    parser.add_argument("--task", default="", help="Task summary. Do not include secrets.")
    parser.add_argument("--expected", default="", help="Expected behavior. Do not include secrets.")
    parser.add_argument("--actual", default="", help="Actual behavior. Do not include secrets.")
    parser.add_argument("--tags", default="", help="Comma-separated feedback tags.")
    parser.add_argument("--source", default="manual", help="Feedback source label.")
    parser.add_argument("--feedback-file", default=str(DEFAULT_FEEDBACK_FILE))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = record_feedback(args)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result["feedback_file"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
