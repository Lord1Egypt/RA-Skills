#!/usr/bin/env python3
"""Print the current public status without advancing time."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.present import summary_lines
from rms.state import load_game
from rms.turn import resolve


def main() -> None:
    parser = argparse.ArgumentParser(description="Real Mars Shot status")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    loaded = load_game(args.user_id)
    if not loaded.get("exists"):
        print(json.dumps({"ok": False, "error": "no save"}))
        sys.exit(2)
    result = resolve(loaded["data"], {"type": "status"})
    result["summary_text"] = "\n".join(summary_lines(loaded["data"]))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
