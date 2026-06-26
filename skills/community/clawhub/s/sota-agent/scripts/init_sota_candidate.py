#!/usr/bin/env python3
"""Create a machine-readable candidate record for a SOTA program."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import sanitize_ref


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--candidate-id", required=True, help="Stable candidate identifier.")
    parser.add_argument("--program-id", required=True, help="Parent program identifier.")
    parser.add_argument("--hypothesis", required=True, help="One-sentence candidate hypothesis.")
    parser.add_argument("--change", action="append", default=[], help="Repeatable change item.")
    parser.add_argument("--risk", action="append", default=[], help="Repeatable risk item.")
    parser.add_argument("--artifact", action="append", default=[], help="Repeatable artifact path or public URL.")
    parser.add_argument("--paper-title", action="append", default=[], help="Repeatable source paper title.")
    parser.add_argument("--paper-url", action="append", default=[], help="Repeatable public paper URL.")
    parser.add_argument("--expected-win", default="", help="Expected measurable win.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_id": args.candidate_id,
        "program_id": args.program_id,
        "hypothesis": args.hypothesis,
        "expected_win": args.expected_win,
        "change_set": args.change,
        "risks": args.risk,
        "source_papers": [
            {"title": title, "url": ""}
            for title in args.paper_title
        ] + [
            {"title": "", "url": sanitize_ref(url)}
            for url in args.paper_url
        ],
        "artifacts": [sanitize_ref(item) for item in args.artifact],
        "evaluation_plan": {
            "smoke_checks": [],
            "benchmark_requirements": [],
            "cost_guardrails": [],
        },
        "status": "idea",
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
