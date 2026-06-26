#!/usr/bin/env python3
"""Create a machine-readable snapshot of a target leaderboard contract."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import sanitize_ref


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Path to the output JSON file.")
    parser.add_argument("--task", required=True, help="Task name.")
    parser.add_argument("--dataset", required=True, help="Dataset name.")
    parser.add_argument("--metric", required=True, help="Primary metric name.")
    parser.add_argument("--split", required=True, help="Named split or evaluation surface.")
    parser.add_argument("--current-sota-label", default="", help="Current leading model or entry.")
    parser.add_argument("--current-sota-score", default="", help="Current leading score.")
    parser.add_argument("--baseline-label", default="", help="Trusted baseline name.")
    parser.add_argument("--baseline-score", default="", help="Trusted baseline score.")
    parser.add_argument("--target-score", default="", help="Campaign target score.")
    parser.add_argument("--source", action="append", default=[], help="Repeatable source URL or note.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "contract": {
            "task": args.task,
            "dataset": args.dataset,
            "metric": args.metric,
            "split": args.split,
        },
        "current_sota": {
            "label": args.current_sota_label,
            "score": args.current_sota_score,
        },
        "baseline": {
            "label": args.baseline_label,
            "score": args.baseline_score,
        },
        "target": {
            "score": args.target_score,
            "claim_status": "unproven",
        },
        "sources": [sanitize_ref(item) for item in args.source],
        "notes": [],
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
