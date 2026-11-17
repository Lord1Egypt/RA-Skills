#!/usr/bin/env python3
"""Resolve one action against a save. The agent supplies structured intent; this does the math."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.state import load_game, save_game
from rms.turn import resolve


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve a Real Mars Shot turn")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--action", help="JSON action. Otherwise stdin.")
    parser.add_argument("--force-roll", type=int)
    parser.add_argument("--force-event", default=None)
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    raw = args.action if args.action is not None else sys.stdin.read()
    action = json.loads(raw)
    loaded = load_game(args.user_id)
    if not loaded.get("exists"):
        print(json.dumps({"ok": False, "error": "no save", "save_path": loaded["save_path"]}, ensure_ascii=False))
        sys.exit(2)
    result = resolve(loaded["data"], action, force_roll=args.force_roll, force_event=args.force_event)
    if result.get("mutated") and not args.no_commit:
        result["save"] = save_game(loaded["data"])
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    if not result.get("ok") and not result.get("needs_confirmation"):
        sys.exit(1)


if __name__ == "__main__":
    main()
