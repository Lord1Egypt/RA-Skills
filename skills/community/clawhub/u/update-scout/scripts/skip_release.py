#!/usr/bin/env python3
"""
scout - skip_release.py
Mark a specific version as skipped so check_updates.py stops surfacing it.

Usage:
  python3 skip_release.py --tool openclaw --version v2026.3.13-1 --reason "Not needed"
  python3 skip_release.py --list
  python3 skip_release.py --clear --tool openclaw

Note: --version must be the exact tag string (e.g. v1.2.3). When a newer release
comes out, it will appear in check_updates again automatically.
"""

import json
import os
import argparse
from datetime import date

from scout_config import DEFAULT_SKIP_PATH


def load_skip_list(path: str) -> dict:
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_skip_list(path: str, data: dict):
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Manage scout skip list")
    parser.add_argument("--tool", help="Tool name")
    parser.add_argument("--version", help="Version to skip (use 'latest' to skip current latest)")
    parser.add_argument("--reason", default="", help="Why skipping")
    parser.add_argument("--list", action="store_true", help="List all skipped versions")
    parser.add_argument("--clear", action="store_true", help="Remove skip entry for a tool")
    parser.add_argument("--config", default=DEFAULT_SKIP_PATH, help="Skip list path")
    args = parser.parse_args()

    skip_list = load_skip_list(args.config)

    if args.list:
        if not skip_list:
            print("No skipped versions.")
        else:
            print("Skipped versions:\n")
            for tool, entry in skip_list.items():
                print(f"  {tool}: {entry['version']} — {entry.get('reason', '(no reason)')} (skipped {entry.get('date', '?')})")
        return

    if not args.tool:
        parser.error("--tool is required")

    if args.clear:
        if args.tool in skip_list:
            del skip_list[args.tool]
            save_skip_list(args.config, skip_list)
            print(f"Cleared skip entry for '{args.tool}'")
        else:
            print(f"No skip entry found for '{args.tool}'")
        return

    if not args.version:
        parser.error("--version is required")

    skip_list[args.tool] = {
        "version": args.version,
        "reason": args.reason,
        "date": str(date.today()),
    }
    save_skip_list(args.config, skip_list)
    print(f"Skipping {args.tool} {args.version}: {args.reason or '(no reason given)'}")


if __name__ == "__main__":
    main()
