from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.feedback import apply_feedback, build_feedback_report
from common import load_json, utc_now_iso, write_json
from memory_store import load_memory, save_memory


def main() -> int:
    parser = argparse.ArgumentParser(description="Review feedback and update memory for future cycles.")
    parser.add_argument("--mission", default="data/mission.json", help="Mission JSON path.")
    parser.add_argument("--feedback", required=True, help="Feedback JSON path.")
    parser.add_argument("--memory", default="data/memory.json", help="Persistent memory JSON path.")
    parser.add_argument("--output", default="data/feedback_report.json", help="Feedback report JSON path.")
    args = parser.parse_args()

    mission = load_json(args.mission)
    feedback = load_json(args.feedback).get("items", [])
    memory = load_memory(args.memory)
    updated_at = utc_now_iso()
    new_memory = apply_feedback(memory, feedback, updated_at)
    save_memory(args.memory, new_memory)

    report = build_feedback_report(mission.get("name"), feedback, new_memory, updated_at)
    output_path = write_json(args.output, report)
    print(f"Wrote feedback report to {output_path}")
    print(report["recommendation"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
