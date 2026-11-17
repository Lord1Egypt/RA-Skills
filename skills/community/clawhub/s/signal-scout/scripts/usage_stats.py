#!/usr/bin/env python3
"""Report repeat-usage patterns across signal-scout runs — local only, no network.

This is a maintainer-facing check, not part of the research workflow:
it answers "does anyone actually come back to the same product?" before
building more on watch mode. Reads only the
outputs/<product-slug>/analysis-<YYYY-MM-DD>.json files the storage
convention in SKILL.md already produces — no telemetry, nothing leaves the
machine.

Usage:
    python3 usage_stats.py [outputs_dir]

Exit code is always 0 — this is a report, not a check.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

DATE_RE = re.compile(r"analysis-(\d{4}-\d{2}-\d{2})\.json$")


def find_runs(outputs_dir: Path) -> dict[str, list[date]]:
    runs: dict[str, list[date]] = {}
    if not outputs_dir.is_dir():
        return runs
    for product_dir in sorted(outputs_dir.iterdir()):
        if not product_dir.is_dir():
            continue
        dates = []
        for f in product_dir.glob("analysis-*.json"):
            m = DATE_RE.search(f.name)
            if m:
                dates.append(date.fromisoformat(m.group(1)))
        if dates:
            runs[product_dir.name] = sorted(dates)
    return runs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outputs_dir", type=Path, nargs="?", default=Path("outputs"))
    args = parser.parse_args()

    runs = find_runs(args.outputs_dir)
    if not runs:
        print(f"No analysis-<date>.json files found under {args.outputs_dir}/<product-slug>/.")
        print("Nothing to report yet — this fills in as products are re-run over time.")
        return

    total_products = len(runs)
    repeat_products = {slug: dates for slug, dates in runs.items() if len(dates) >= 2}
    total_runs = sum(len(dates) for dates in runs.values())

    print(f"{'PRODUCT':<32} {'RUNS':<6} {'FIRST':<12} {'LATEST':<12} {'SPAN (days)':<12}")
    for slug, dates in runs.items():
        span = (dates[-1] - dates[0]).days
        print(f"{slug:<32} {len(dates):<6} {dates[0].isoformat():<12} {dates[-1].isoformat():<12} {span:<12}")

    repeat_rate = (len(repeat_products) / total_products * 100) if total_products else 0.0
    print(
        f"\n{total_products} product(s) tracked, {total_runs} total run(s), "
        f"{len(repeat_products)} product(s) re-run at least once ({repeat_rate:.0f}% repeat rate)."
    )
    if repeat_products:
        gaps = [
            (dates[i + 1] - dates[i]).days
            for dates in repeat_products.values()
            for i in range(len(dates) - 1)
        ]
        avg_gap = sum(gaps) / len(gaps)
        print(f"Average gap between repeat runs on the same product: {avg_gap:.1f} days.")
        print(
            "Watch mode is worth more work once this repeat rate and gap are "
            "stable across enough products to trust — a single repeat run is a data point, "
            "not a pattern."
        )
    else:
        print(
            "No repeat runs yet. Don't build more on watch mode off this alone — "
            "every run so far has been a one-off check, which the one-shot report "
            "already serves."
        )


if __name__ == "__main__":
    main()
