from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.execution import preflight_action
from common import load_json, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight an X action to reduce avoidable 403 failures.")
    parser.add_argument("--action", default="data/action.json", help="Action JSON path.")
    parser.add_argument("--output", help="Optional output JSON path for the preflight result.")
    args = parser.parse_args()

    action = load_json(args.action)
    result = preflight_action(action)

    if args.output:
        write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["decision"] != "block" else 2


if __name__ == "__main__":
    raise SystemExit(main())
