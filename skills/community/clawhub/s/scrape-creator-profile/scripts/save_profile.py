#!/usr/bin/env python3
"""
save_profile.py — Save a scraped creator profile JSON to disk.

Usage:
    python3 save_profile.py --data '<json string>' --output ~/creator-profiles/mkbhd_youtube.json
    python3 save_profile.py --data '<json string>'   # auto-names file from handle + platform
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def auto_filename(profile: dict) -> str:
    handle = profile.get("handle", "unknown").lstrip("@").lower()
    platform = profile.get("platform", "unknown").lower()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{handle}_{platform}_{ts}.json"


def main():
    parser = argparse.ArgumentParser(description="Save a creator profile JSON to disk.")
    parser.add_argument("--data", required=True, help="JSON string of the profile")
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path. Auto-generated from handle+platform if not specified.",
    )
    args = parser.parse_args()

    try:
        profile = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else Path.home() / "creator-profiles" / auto_filename(profile)
    output_path = output_path.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
