#!/usr/bin/env python3
"""Create a review packet that joins the key artifacts for a SOTA decision."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import sanitize_ref


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--program-id", required=True, help="Program identifier.")
    parser.add_argument("--candidate-id", required=True, help="Candidate identifier.")
    parser.add_argument("--program", default="", help="Program JSON path.")
    parser.add_argument("--candidate", default="", help="Candidate JSON path.")
    parser.add_argument("--ablation-queue", default="", help="Ablation queue JSON path.")
    parser.add_argument("--scoreboard", default="", help="Scoreboard JSON path.")
    parser.add_argument("--paper", action="append", default=[], help="Repeatable paper title or public URL.")
    parser.add_argument("--artifact", action="append", default=[], help="Repeatable artifact path or URL.")
    parser.add_argument("--decision", default="hold", help="promote, hold, or cut.")
    parser.add_argument("--reason", default="", help="Benchmark-backed decision reason.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "program_id": args.program_id,
        "candidate_id": args.candidate_id,
        "artifacts": {
            "program": sanitize_ref(args.program),
            "candidate": sanitize_ref(args.candidate),
            "ablation_queue": sanitize_ref(args.ablation_queue),
            "scoreboard": sanitize_ref(args.scoreboard),
            "papers": [sanitize_ref(item) for item in args.paper],
            "supporting_artifacts": [sanitize_ref(item) for item in args.artifact],
        },
        "decision": {
            "status": args.decision,
            "reason": args.reason,
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
