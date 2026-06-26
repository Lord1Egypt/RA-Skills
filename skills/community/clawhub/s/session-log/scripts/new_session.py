#!/usr/bin/env python3
"""Create a new session log file with the current local timestamp."""

import argparse
import os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))

def main():
    parser = argparse.ArgumentParser(description="Create a new session log file")
    parser.add_argument("--agent", default="main", help="Agent name (main/writer/coding)")
    parser.add_argument("--dir", required=True, help="Directory to write session file into")
    args = parser.parse_args()

    now = datetime.now(CST)
    filename = now.strftime(f"%Y-%m-%d_%H-%M_{args.agent}.md")
    header = now.strftime(f"# Session %Y-%m-%d %H:%M | {args.agent}\n\n## Log\n\n")

    os.makedirs(args.dir, exist_ok=True)
    filepath = os.path.join(args.dir, filename)

    if os.path.exists(filepath):
        print(f"[skip] Already exists: {filepath}")
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header)
        print(f"[ok] Created: {filepath}")

if __name__ == "__main__":
    main()
