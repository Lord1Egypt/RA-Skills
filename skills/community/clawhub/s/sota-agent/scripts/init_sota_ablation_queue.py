#!/usr/bin/env python3
"""Create a machine-readable ablation queue for one SOTA candidate family."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_ablation(item: str) -> dict[str, object]:
    if "=" not in item:
        raise SystemExit(f"invalid --ablation value: {item!r}, expected id=description")
    ablation_id, description = item.split("=", 1)
    return {
        "ablation_id": ablation_id.strip(),
        "description": description.strip(),
        "priority": 0,
        "status": "pending",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--program-id", required=True, help="Parent program identifier.")
    parser.add_argument("--candidate-id", required=True, help="Candidate identifier.")
    parser.add_argument("--ablation", action="append", default=[], help="Repeatable id=description item.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "program_id": args.program_id,
        "candidate_id": args.candidate_id,
        "items": [parse_ablation(item) for item in args.ablation],
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
