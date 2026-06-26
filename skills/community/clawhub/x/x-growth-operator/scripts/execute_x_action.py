from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.execution import build_x_command, run_x_action
from common import load_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute an action.json against the X OAuth CLI.")
    parser.add_argument("--action", default="data/action.json", help="Action JSON path.")
    parser.add_argument("--print-command", action="store_true", help="Print the underlying command instead of executing.")
    args = parser.parse_args()

    action = load_json(args.action)
    cmd = build_x_command(action)
    if args.print_command:
        print(" ".join(json.dumps(part) for part in cmd))
        return 0

    print(run_x_action(action))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
