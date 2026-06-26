#!/usr/bin/env python3
"""Create or refresh a sorted scoreboard for SOTA candidates on one fixed metric."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_entry(item: str) -> dict[str, object]:
    if "=" not in item:
        raise SystemExit(f"invalid --entry value: {item!r}, expected candidate=score[,key=value...]")
    candidate_id, rest = item.split("=", 1)
    parts = [chunk.strip() for chunk in rest.split(",") if chunk.strip()]
    if not parts:
        raise SystemExit(f"invalid --entry value: {item!r}, missing score")

    score = float(parts[0])
    record: dict[str, object] = {
        "candidate_id": candidate_id.strip(),
        "score": score,
        "stage": "",
        "status": "",
        "notes": "",
    }
    for part in parts[1:]:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        record[key.strip()] = value.strip()
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--metric-name", required=True, help="Metric shared by every entry.")
    parser.add_argument("--entry", action="append", default=[], help="Repeatable candidate=score[,key=value...] item.")
    parser.add_argument("--minimize", action="store_true", default=False, help="Treat lower scores as better.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    entries = [parse_entry(item) for item in args.entry]
    entries.sort(key=lambda item: float(item["score"]), reverse=not args.minimize)
    if entries:
        best_score = float(entries[0]["score"])
    else:
        best_score = 0.0

    for index, item in enumerate(entries, start=1):
        score = float(item["score"])
        item["rank"] = index
        item["delta_to_best"] = score - best_score

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "metric_name": args.metric_name,
        "goal_direction": "minimize" if args.minimize else "maximize",
        "best_candidate": entries[0]["candidate_id"] if entries else "",
        "entries": entries,
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
