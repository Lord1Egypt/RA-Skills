from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common import load_json
from core.mission import mission_search_query


def run_step(cmd: list[str]) -> None:
    completed = subprocess.run(cmd, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search X via Desearch, score opportunities, and build an action plan.")
    parser.add_argument("--mission", default="data/mission.json", help="Mission JSON path.")
    parser.add_argument("--query", help="Live X search query. If omitted, derive it from the mission.")
    parser.add_argument("--count", type=int, default=10, help="Result count.")
    parser.add_argument("--sort", choices=["Top", "Latest"], default="Latest", help="Desearch sort order.")
    parser.add_argument("--opportunities-out", default="data/opportunities_from_desearch.json", help="Imported opportunities path.")
    parser.add_argument("--scored-out", default="data/opportunities_scored.json", help="Scored opportunities path.")
    parser.add_argument("--plan-out", default="data/action_plan.json", help="Action plan path.")
    args = parser.parse_args()

    mission = load_json(args.mission)
    query = args.query or mission_search_query(mission)
    if not query:
        parser.error("Could not derive a live search query from the mission. Provide --query.")

    run_step([
        "python3",
        "scripts/import_desearch.py",
        "x",
        query,
        "--count",
        str(args.count),
        "--sort",
        args.sort,
        "--output",
        args.opportunities_out,
    ])
    run_step([
        "python3",
        "scripts/watch_x.py",
        "--mission",
        args.mission,
        "--input",
        args.opportunities_out,
        "--memory",
        "data/memory.json",
        "--output",
        args.scored_out,
    ])
    run_step([
        "python3",
        "scripts/plan_actions.py",
        "--mission",
        args.mission,
        "--opportunities",
        args.scored_out,
        "--output",
        args.plan_out,
    ])
    print(f"Used query: {query}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
