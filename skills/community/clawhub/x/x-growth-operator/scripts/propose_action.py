from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.drafting import build_draft
from core.storage import LocalStateStore
from common import load_json, utc_now_iso


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a proposed X action from a scored opportunity.")
    parser.add_argument("--mission", default="data/mission.json", help="Mission JSON path.")
    parser.add_argument("--opportunities", default="data/opportunities_scored.json", help="Scored opportunities JSON path.")
    parser.add_argument("--opportunity-id", required=True, help="Opportunity id to act on.")
    parser.add_argument("--output", default="data/action.json", help="Output action JSON path.")
    args = parser.parse_args()

    mission = load_json(args.mission)
    opportunities = load_json(args.opportunities).get("items", [])
    opportunity = next((item for item in opportunities if item.get("id") == args.opportunity_id), None)
    if not opportunity:
        raise SystemExit(f"Opportunity not found: {args.opportunity_id}")

    draft, rationale = build_draft(mission, opportunity)
    action = {
        "id": f"action-{opportunity['id']}",
        "created_at": utc_now_iso(),
        "status": "proposed",
        "mission_name": mission.get("name", ""),
        "opportunity_id": opportunity["id"],
        "action_type": opportunity.get("recommended_action", "observe"),
        "target_url": opportunity.get("url", ""),
        "target_account": opportunity.get("source_account", ""),
        "risk_level": opportunity.get("risk_level", "medium"),
        "score": opportunity.get("score", 0),
        "draft_text": draft,
        "rationale": rationale,
        "requires_approval": True,
    }
    output_path = LocalStateStore(Path(args.output).parent).save_action(action, Path(args.output).name)

    print(f"Wrote action to {output_path}")
    print(f"Action: {action['action_type']} score={action['score']} risk={action['risk_level']}")
    if action["draft_text"]:
        print(action["draft_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
