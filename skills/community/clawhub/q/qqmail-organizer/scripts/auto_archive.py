#!/usr/bin/env python3
"""
Compatibility wrapper for old qqmail auto-archive calls.

The organization engine now lives in qqmail.py so decoding, rules, dry-run, and
safety behavior stay in one place.
"""

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="QQ Mail Auto-Archive compatibility wrapper")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving")
    parser.add_argument("--apply", action="store_true", help="Actually apply archive/mark rules")
    parser.add_argument("--limit", type=int, default=100, help="Number of recent emails to evaluate")
    parser.add_argument("--folder", default="INBOX", help="Source folder")
    parser.add_argument("--rules", help="Rules JSON path")
    args = parser.parse_args()

    script = os.path.join(os.path.dirname(__file__), "qqmail.py")
    cmd = [
        sys.executable,
        script,
        "auto-organize",
        "--limit",
        str(args.limit),
        "--folder",
        args.folder,
    ]
    if args.rules:
        cmd.extend(["--rules", args.rules])
    if args.apply and not args.dry_run:
        cmd.append("--apply")

    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
