#!/usr/bin/env python3
import argparse
import datetime as dt
import json
from pathlib import Path

from replay_common import DEFAULT_REPLAY_FILE, append_jsonl, load_jsonl, redact_text, stable_id


def traits_from_entry(entry: dict) -> list[str]:
    text = " ".join(str(entry.get(key) or "") for key in ["feedback", "expected", "task"]).lower()
    traits = []
    if any(term in text for term in ["citation", "reference", "apa", "mla", "literature"]):
        traits.extend(["structured academic output", "no fabricated citations", "missing metadata flagged"])
    if any(term in text for term in ["prd", "mvp", "acceptance", "roadmap"]):
        traits.extend(["clear mvp scope", "testable acceptance criteria", "implementation handoff"])
    if any(term in text for term in ["api", "token", "webhook", "integration", "telegram", "notion"]):
        traits.extend(["credential safety", "health check", "failure handling"])
    if any(term in text for term in ["script", "cli", "export", "validate", "batch"]):
        traits.extend(["deterministic script contract", "input validation", "failure modes"])
    return sorted(set(traits)) or ["clear structure", "explicit assumptions", "actionable output"]


def case_from_feedback(entry: dict) -> dict:
    task = entry.get("task") or entry.get("feedback") or "No task supplied."
    expected = entry.get("expected") or entry.get("feedback") or ""
    actual = entry.get("actual") or ""
    redacted_task = redact_text(str(task))
    return {
        "id": stable_id(entry.get("skill", ""), redacted_task, str(entry.get("created_at", ""))),
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "feedback",
        "agent": entry.get("agent"),
        "skill": entry.get("skill"),
        "task": redacted_task,
        "expected_traits": traits_from_entry(entry),
        "expected": redact_text(str(expected)),
        "previous_actual": redact_text(str(actual)),
        "privacy": "redacted",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect redacted replay cases from skill feedback.")
    parser.add_argument("--feedback-file", required=True)
    parser.add_argument("--output", default=str(DEFAULT_REPLAY_FILE))
    parser.add_argument("--skill", default="")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    feedback = load_jsonl(Path(args.feedback_file).expanduser())
    if args.skill:
        feedback = [entry for entry in feedback if entry.get("skill") == args.skill]
    cases = [case_from_feedback(entry) for entry in feedback[-args.limit:] if entry.get("skill")]
    output = Path(args.output).expanduser()
    existing_ids = {row.get("id") for row in load_jsonl(output)}
    new_cases = [case for case in cases if case["id"] not in existing_ids]
    append_jsonl(output, new_cases)
    payload = {"status": "ok", "cases_written": len(new_cases), "output": str(output)}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
