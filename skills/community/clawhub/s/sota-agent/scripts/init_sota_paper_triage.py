#!/usr/bin/env python3
"""Create a machine-readable paper triage queue for a SOTA campaign."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Path to the output JSON file.")
    parser.add_argument("--campaign-id", required=True, help="Campaign identifier.")
    parser.add_argument("--task", required=True, help="Task name.")
    parser.add_argument("--paper", action="append", default=[], help="Repeatable paper title seed.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    papers = []
    for title in args.paper:
        papers.append(
            {
                "title": title,
                "bucket": "must-read",
                "year": "",
                "source_url": "",
                "metric_claim": "",
                "compute_notes": "",
                "transferable_idea": "",
                "cheapest_test": "",
                "reproduction_status": "unread",
            }
        )

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "campaign_id": args.campaign_id,
        "task": args.task,
        "papers": papers,
        "notes": [],
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
