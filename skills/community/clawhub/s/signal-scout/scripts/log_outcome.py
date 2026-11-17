#!/usr/bin/env python3
"""Log what actually happened to a signal-scout prospect after outreach.

This is the ground-truth input the scoring model doesn't otherwise get. Every
score signal-scout produces is the model grading its own evidence; this log
is the only place a real outcome — did the reply come, did the deal close —
enters the loop. `recalibrate.py` reads this file to suggest which query
buckets and source types to weight up or down on the next run for the same
product.

Usage:
    # Log one outcome
    python3 log_outcome.py outcomes.jsonl --name "jdoe" --type individual \\
        --source-type "Forum" --query-bucket pain --score 82 \\
        --outcome replied --date 2026-07-14 --source-url "https://..."

    # List everything logged so far
    python3 log_outcome.py outcomes.jsonl --list

`--outcome` must be one of: replied, no_reply, converted, not_pursued.
Appends one JSON line per call — safe to run repeatedly, never overwrites.

Pass `--source-url` when you have it. `diff_reports.py --outcomes` matches
resurfacing prospects back to logged outcomes by (name, source_url) when
both are available, falling back to name only otherwise — so recording it
tells "Alex Chen who posted about pricing" apart from "Alex Chen who posted
about onboarding" instead of merging them into one name.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID_OUTCOMES = {"replied", "no_reply", "converted", "not_pursued"}
VALID_TYPES = {"individual", "segment", "company"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("log_path", type=Path, help="Path to outcomes.jsonl (created if missing)")
    parser.add_argument("--list", action="store_true", help="Print all logged outcomes and exit")
    parser.add_argument("--name")
    parser.add_argument("--type", choices=sorted(VALID_TYPES))
    parser.add_argument("--source-type", help="e.g. Forum, GitHub issue, Job post — from the prospect's source_type")
    parser.add_argument("--query-bucket", help="Which query bucket surfaced this prospect, e.g. pain, switching, timing")
    parser.add_argument("--score", type=int, help="The score signal-scout assigned (0-100)")
    parser.add_argument("--outcome", choices=sorted(VALID_OUTCOMES))
    parser.add_argument("--date", help="ISO date the outcome was observed, e.g. 2026-07-14")
    parser.add_argument("--source-url", default="", help="The prospect's source_url — disambiguates same-name prospects when diff_reports.py --outcomes matches against this log")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    if args.list:
        if not args.log_path.exists():
            print("No outcomes logged yet.")
            return
        rows = [json.loads(line) for line in args.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not rows:
            print("No outcomes logged yet.")
            return
        print(f"{'DATE':<12} {'TYPE':<10} {'NAME':<24} {'SOURCE':<16} {'BUCKET':<12} {'SCORE':<6} OUTCOME")
        for row in rows:
            print(
                f"{row.get('date', ''):<12} {row.get('type', ''):<10} {str(row.get('name', ''))[:24]:<24} "
                f"{str(row.get('source_type', ''))[:16]:<16} {str(row.get('query_bucket', ''))[:12]:<12} "
                f"{row.get('score', ''):<6} {row.get('outcome', '')}"
            )
        print(f"\n{len(rows)} outcomes logged.")
        return

    missing = [flag for flag, val in [("--name", args.name), ("--type", args.type), ("--outcome", args.outcome), ("--date", args.date)] if not val]
    if missing:
        parser.error(f"missing required flags for logging a record: {', '.join(missing)}")

    record = {
        "name": args.name,
        "type": args.type,
        "source_type": args.source_type or "",
        "query_bucket": args.query_bucket or "",
        "score": args.score,
        "outcome": args.outcome,
        "date": args.date,
        "source_url": args.source_url,
        "notes": args.notes,
    }

    args.log_path.parent.mkdir(parents=True, exist_ok=True)
    with args.log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    print(f"Logged: {args.name} ({args.type}) → {args.outcome}")


if __name__ == "__main__":
    main()
