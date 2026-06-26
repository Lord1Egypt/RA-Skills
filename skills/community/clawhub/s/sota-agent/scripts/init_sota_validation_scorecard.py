#!/usr/bin/env python3
"""Create a machine-readable validation scorecard for browser or notebook checks."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import sanitize_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Path to the output JSON file.")
    parser.add_argument("--scorecard-id", required=True, help="Stable validation scorecard identifier.")
    parser.add_argument("--candidate-id", default="", help="Optional candidate identifier.")
    parser.add_argument("--surface", default="", help="Surface under review such as pseudo-label QA or aug-preview.")
    parser.add_argument("--workflow", default="", help="Workflow label such as colab-smoke or kaggle-preview.")
    parser.add_argument("--evidence-root", default="", help="Optional local evidence root.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    evidence_root = args.evidence_root.strip()
    if evidence_root:
        evidence_root = sanitize_path(evidence_root, allow_absolute_paths=False)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scorecard_id": args.scorecard_id,
        "candidate_id": args.candidate_id,
        "surface": args.surface,
        "workflow": args.workflow,
        "evidence_root": evidence_root,
        "items": [],
        "summary": {
            "pass_count": 0,
            "fail_count": 0,
            "average_score": None,
        },
        "notes": [],
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
