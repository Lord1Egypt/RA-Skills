#!/usr/bin/env python3
"""Create a machine-readable candidate card for a serious SOTA attempt."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Path to the output JSON file.")
    parser.add_argument("--candidate-id", required=True, help="Stable candidate identifier.")
    parser.add_argument("--campaign-id", required=True, help="Parent campaign identifier.")
    parser.add_argument("--objective", required=True, help="Short statement of what the candidate tries to prove.")
    parser.add_argument("--baseline", default="", help="Trusted baseline identifier.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.2",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "campaign_id": args.campaign_id,
        "candidate_id": args.candidate_id,
        "objective": args.objective,
        "baseline": args.baseline,
        "hypothesis": {
            "summary": "",
            "novelty_type": "",
            "borrowed_from": [],
        },
        "execution": {
            "lane": "",
            "auth_mode": "local_or_artifact_only",
            "compute_budget": "",
            "wall_time_budget": "",
            "critical_ablation_question": "",
            "agent_threads": [],
        },
        "evaluation": {
            "benchmark_contract_path": "",
            "score": "",
            "delta_vs_baseline": "",
            "slice_scores": {},
            "reruns": [],
            "failure_cases": [],
            "regression_notes": [],
            "review_dashboard_path": "",
            "claim_safety_paths": [],
            "review_packet_path": "",
        },
        "claim_review": {
            "status": "hold",
            "wording": "",
            "blocked_by": [],
            "evidence_paths": [],
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
