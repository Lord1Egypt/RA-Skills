#!/usr/bin/env python3
"""Write a save from a JSON object on stdin or --data. Prefer resolve_turn.py during play."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.state import save_game


def main() -> None:
    parser = argparse.ArgumentParser(description="Save a Real Mars Shot state")
    parser.add_argument("--data")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()
    raw = args.data if args.data is not None else sys.stdin.read()
    state = json.loads(raw)
    if "user_id" not in state:
        print(json.dumps({"success": False, "error": "state.user_id required"}))
        sys.exit(1)
    result = save_game(state, backup=not args.no_backup)
    if args.quiet:
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
