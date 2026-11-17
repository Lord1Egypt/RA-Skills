#!/usr/bin/env python3
"""Load a save. Secrets are omitted unless --internal is set (engine only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.present import summary_lines
from rms.state import load_game, public_view


def main() -> None:
    parser = argparse.ArgumentParser(description="Load a Real Mars Shot save")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--internal", action="store_true", help="include secrets; do not show this to the player")
    args = parser.parse_args()
    loaded = load_game(args.user_id)
    if loaded.get("exists") and not args.internal:
        loaded["data"] = public_view(loaded["data"])
        loaded["summary_lines"] = summary_lines(loaded["data"])
    print(json.dumps(loaded, ensure_ascii=False, indent=2 if args.pretty else None))
    if not loaded.get("exists"):
        sys.exit(2)


if __name__ == "__main__":
    main()
