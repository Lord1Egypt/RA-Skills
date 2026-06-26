from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common import load_json, load_local_env
from core.mission import mission_search_query

def run_step(args: list[str]) -> None:
    completed = subprocess.run(args, cwd=ROOT, check=True)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    load_local_env()
    parser = argparse.ArgumentParser(description="Run the local X growth cycle end to end.")
    parser.add_argument("--doc", help="Mission brief document path.")
    parser.add_argument("--prompt", help="Inline mission prompt.")
    parser.add_argument("--opportunities", help="Opportunities JSON path.")
    parser.add_argument("--live-query", help="Optional Desearch live search query to generate opportunities instead of --opportunities. If omitted, derive it from the mission.")
    parser.add_argument("--feedback", help="Optional feedback JSON path.")
    parser.add_argument("--mission", default="data/mission.json", help="Mission JSON output path.")
    parser.add_argument("--memory", default="data/memory.json", help="Memory JSON path.")
    args = parser.parse_args()

    if not args.doc and not args.prompt and not Path(args.mission).exists():
        parser.error("Provide --doc or --prompt, or ensure --mission already exists.")
    if not args.opportunities and not Path(args.mission).exists() and not (args.doc or args.prompt):
        parser.error("Provide --opportunities or a mission source that can generate a live query.")

    if args.doc or args.prompt:
        cmd = ["python3", "scripts/ingest_goal.py", "--mission", args.mission]
        if args.doc:
            cmd.extend(["--doc", args.doc])
        else:
            cmd.extend(["--prompt", args.prompt])
        run_step(cmd)

    opportunities_input = args.opportunities
    if args.live_query or not args.opportunities:
        opportunities_input = "data/opportunities_from_desearch.json"
        mission = load_json(args.mission)
        query = args.live_query or mission_search_query(mission)
        if not query:
            raise SystemExit("Could not derive a live search query from the mission.")
        run_step([
            "python3",
            "scripts/import_desearch.py",
            "x",
            query,
            "--count",
            "10",
            "--output",
            opportunities_input,
        ])

    run_step([
        "python3",
        "scripts/watch_x.py",
        "--mission",
        args.mission,
        "--input",
        opportunities_input,
        "--output",
        "data/opportunities_scored.json",
        "--memory",
        args.memory,
    ])
    run_step([
        "python3",
        "scripts/plan_actions.py",
        "--mission",
        args.mission,
        "--opportunities",
        "data/opportunities_scored.json",
        "--output",
        "data/action_plan.json",
    ])

    if args.feedback:
        run_step([
            "python3",
            "scripts/review_feedback.py",
            "--mission",
            args.mission,
            "--feedback",
            args.feedback,
            "--memory",
            args.memory,
            "--output",
            "data/feedback_report.json",
        ])

    print("Cycle complete. Review data/action_plan.json and data/feedback_report.json if present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
