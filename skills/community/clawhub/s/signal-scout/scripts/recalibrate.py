#!/usr/bin/env python3
"""Turn logged outcomes into query-bucket and source-type weighting suggestions.

Reads the outcomes.jsonl produced by log_outcome.py and computes, per source
type and per query bucket, what fraction of logged prospects actually
replied or converted versus went cold. Prints suggestions to weight future
research toward buckets/sources with above-average hit rates and away from
ones that consistently produced dead ends — this is the only place actual
outcome data feeds back into how the next research run is steered.

Requires at least --min-samples (default 3) logged outcomes for a bucket or
source type before making a suggestion about it; below that, prints the raw
counts without a recommendation, since 1-2 data points aren't a pattern.

Usage:
    python3 recalibrate.py outcomes.jsonl [--min-samples 3]
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

POSITIVE_OUTCOMES = {"replied", "converted"}


def hit_rate(rows: list[dict[str, Any]]) -> float:
    decided = [r for r in rows if r.get("outcome") != "not_pursued"]
    if not decided:
        return 0.0
    hits = sum(1 for r in decided if r.get("outcome") in POSITIVE_OUTCOMES)
    return hits / len(decided)


def summarize(rows: list[dict[str, Any]], key: str, min_samples: int) -> list[tuple[str, int, float]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        value = str(row.get(key) or "").strip()
        if value:
            grouped[value].append(row)
    return sorted(
        ((name, len(items), hit_rate(items)) for name, items in grouped.items()),
        key=lambda entry: entry[2],
        reverse=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("log_path", type=Path)
    parser.add_argument("--min-samples", type=int, default=3)
    args = parser.parse_args()

    if not args.log_path.exists():
        print("No outcomes logged yet — nothing to recalibrate. Log outcomes with log_outcome.py first.")
        return

    rows = [json.loads(line) for line in args.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        print("Outcomes file is empty — nothing to recalibrate.")
        return

    overall = hit_rate(rows)
    print(f"Overall hit rate (replied + converted, excluding not_pursued): {overall:.0%} across {len(rows)} logged prospects.\n")

    for label, key in (("source type", "source_type"), ("query bucket", "query_bucket")):
        print(f"By {label}:")
        summary = summarize(rows, key, args.min_samples)
        if not summary:
            print("  (none logged)\n")
            continue
        for name, count, rate in summary:
            if count < args.min_samples:
                print(f"  {name:<24} n={count:<3} {rate:>5.0%}  (below --min-samples={args.min_samples}, no recommendation yet)")
                continue
            if rate >= overall + 0.15:
                verdict = "WEIGHT UP — outperforming average"
            elif rate <= overall - 0.15:
                verdict = "WEIGHT DOWN — underperforming average"
            else:
                verdict = "on par with average"
            print(f"  {name:<24} n={count:<3} {rate:>5.0%}  {verdict}")
        print()

    print("Apply suggestions by prioritizing WEIGHT UP buckets/sources first in the next research pass,")
    print("and treating WEIGHT DOWN ones as lower-confidence even at a high self-graded score.")


if __name__ == "__main__":
    main()
