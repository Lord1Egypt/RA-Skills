#!/usr/bin/env python3
"""Append one application event to app_timeline.jsonl in the project directory. See reference/deploy/14_app_timeline.md"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

EVENTS = ("deploy", "hotfix", "observe", "operate")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True,
                    help="writer: qwencloud-deploy / qwencloud-observe / qwencloud-operate")
    ap.add_argument("--event", required=True, choices=EVENTS)
    ap.add_argument("--summary", required=True, help="one-line human-readable summary")
    ap.add_argument("--data-json", default=None,
                    help="JSON object of event-specific fields, merged into the record (no passwords/signed URLs)")
    ap.add_argument("--project-root", default=".")
    args = ap.parse_args()

    entry = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "skill": args.skill,
        "event": args.event,
        "summary": args.summary,
    }
    if args.data_json:
        extra = json.loads(args.data_json)
        if not isinstance(extra, dict):
            sys.exit("--data-json must be a JSON object")
        entry.update(extra)

    path = Path(args.project_root).resolve() / "app_timeline.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    os.chmod(path, 0o600)
    print(str(path))


if __name__ == "__main__":
    main()
