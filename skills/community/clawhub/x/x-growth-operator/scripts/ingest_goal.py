from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.mission import mission_from_text
from core.storage import LocalStateStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a mission.json from a brief or prompt.")
    parser.add_argument("--doc", help="Path to a source brief or uploaded document text export.")
    parser.add_argument("--prompt", help="Inline natural language mission prompt.")
    parser.add_argument("--mission", default="data/mission.json", help="Output mission JSON path.")
    args = parser.parse_args()

    if not args.doc and not args.prompt:
        parser.error("Provide either --doc or --prompt.")

    raw_text = args.prompt or Path(args.doc).read_text(encoding="utf-8")
    mission = mission_from_text(raw_text)
    output_path = LocalStateStore(Path(args.mission).parent).save_mission(mission, Path(args.mission).name)

    print(f"Wrote mission to {output_path}")
    print(f"Mission goal: {mission['goal']}")
    print(f"Watching {len(mission['watch_accounts'])} accounts and {len(mission['watch_keywords'])} keywords")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
