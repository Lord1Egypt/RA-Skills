from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.planning import rank_actions
from common import load_json, utc_now_iso, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a ranked action plan from scored X opportunities.")
    parser.add_argument("--mission", default="data/mission.json", help="Mission JSON path.")
    parser.add_argument("--opportunities", default="data/opportunities_scored.json", help="Scored opportunities JSON path.")
    parser.add_argument("--output", default="data/action_plan.json", help="Output action plan JSON path.")
    parser.add_argument("--top", type=int, default=5, help="Maximum planned actions.")
    args = parser.parse_args()

    mission = load_json(args.mission)
    opportunities = load_json(args.opportunities).get("items", [])
    plan_items = rank_actions(mission, opportunities)[: args.top]

    payload = {
        "generated_at": utc_now_iso(),
        "mission_name": mission.get("name"),
        "count": len(plan_items),
        "items": plan_items,
    }
    output_path = write_json(args.output, payload)
    print(f"Wrote {len(plan_items)} planned actions to {output_path}")
    for item in plan_items:
        print(f"- {item['priority']} {item['action_type']} for {item['target_account']} score={item['score']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
