#!/usr/bin/env python3
"""
update-heartbeat.py — Worker utility to update its progress/heartbeat file.
Workers call this after every URL fetch.

Usage:
  python3 update-heartbeat.py <data_dir> <worker_name> \
    --phase fetching \
    --pct 45 \
    --urls-found 20 \
    --urls-fetched 9 \
    --findings 4 \
    --current-url "https://example.com"
"""

import argparse
import json
import os
import time
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("data_dir")
    p.add_argument("worker_name")
    p.add_argument("--phase", default="fetching",
                   choices=["searching", "fetching", "complete"])
    p.add_argument("--pct", type=int, default=0)
    p.add_argument("--urls-found", type=int, default=0)
    p.add_argument("--urls-fetched", type=int, default=0)
    p.add_argument("--findings", type=int, default=0)
    p.add_argument("--current-url", default="")
    args = p.parse_args()

    workers_dir = Path(args.data_dir) / "workers"
    workers_dir.mkdir(parents=True, exist_ok=True)

    progress_file = workers_dir / f"{args.worker_name}-progress.json"

    # Load existing to preserve any fields not being updated
    existing = {}
    if progress_file.exists():
        try:
            existing = json.loads(progress_file.read_text())
        except Exception:
            pass

    existing.update({
        "worker": args.worker_name,
        "phase": args.phase,
        "pct": args.pct,
        "urls_found": args.urls_found,
        "urls_fetched": args.urls_fetched,
        "findings": args.findings,
        "current_url": args.current_url,
        "heartbeat": int(time.time()),
    })

    progress_file.write_text(json.dumps(existing, indent=2))
    print(f"Updated: {progress_file}")

if __name__ == "__main__":
    main()
