from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common import load_json, utc_now_iso, write_json
from core.scoring import score_opportunity
from memory_store import load_memory


def main() -> int:
    parser = argparse.ArgumentParser(description="Score imported X opportunities against a mission.")
    parser.add_argument("--mission", default="data/mission.json", help="Mission JSON path.")
    parser.add_argument("--input", required=True, help="Input opportunities JSON path.")
    parser.add_argument("--output", default="data/opportunities_scored.json", help="Output scored opportunities path.")
    parser.add_argument("--memory", default="data/memory.json", help="Optional memory JSON path.")
    parser.add_argument("--top", type=int, default=10, help="Max opportunities to keep.")
    args = parser.parse_args()

    mission = load_json(args.mission)
    payload = load_json(args.input)
    memory = load_memory(args.memory)
    items = payload.get("items", [])

    scored = [score_opportunity(mission, item, memory=memory) for item in items]
    ranked = sorted(scored, key=lambda item: item["score"], reverse=True)[: args.top]

    output = {
        "generated_at": utc_now_iso(),
        "mission_name": mission.get("name", ""),
        "count": len(ranked),
        "items": ranked,
    }
    output_path = write_json(args.output, output)

    print(f"Wrote {len(ranked)} scored opportunities to {output_path}")
    for item in ranked[:3]:
        print(f"- {item['id']}: score={item['score']} action={item['recommended_action']} risk={item['risk_level']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
