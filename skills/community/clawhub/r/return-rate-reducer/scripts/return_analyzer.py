#!/usr/bin/env python3
"""
Parse a returns CSV and output a return-rate report.

Expects columns: order_id, product, reason, order_date, return_date.
Groups by product and reason, flags products above a return-rate threshold,
and estimates cost impact.

Usage:
    python3 scripts/return_analyzer.py --in returns.csv --threshold 10 --out report.md
    python3 scripts/return_analyzer.py --in returns.csv --threshold 10
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, NamedTuple


class ReturnRow(NamedTuple):
    order_id: str
    product: str
    reason: str
    order_date: str
    return_date: str


DEFAULT_COST_PER_RETURN = 12.0


def read_csv(path: Path) -> List[ReturnRow]:
    rows: List[ReturnRow] = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(ReturnRow(
                order_id=row.get("order_id", "").strip(),
                product=row.get("product", "").strip(),
                reason=row.get("reason", "").strip(),
                order_date=row.get("order_date", "").strip(),
                return_date=row.get("return_date", "").strip(),
            ))
    return rows


def analyze(rows: List[ReturnRow], total_orders: int, threshold: float, cost: float) -> str:
    product_returns: Dict[str, int] = Counter()
    reason_counts: Dict[str, int] = Counter()
    product_reasons: Dict[str, Counter] = defaultdict(Counter)

    for row in rows:
        product_returns[row.product] += 1
        reason_counts[row.reason] += 1
        product_reasons[row.product][row.reason] += 1

    total_returns = len(rows)
    overall_rate = (total_returns / total_orders * 100) if total_orders else 0
    estimated_cost = total_returns * cost

    lines: List[str] = []
    lines.append("# Return Rate Analysis Report\n")

    lines.append("## Overview\n")
    lines.append(f"- **Total orders**: {total_orders:,}")
    lines.append(f"- **Total returns**: {total_returns:,}")
    lines.append(f"- **Overall return rate**: {overall_rate:.1f}%")
    lines.append(f"- **Estimated monthly return cost**: ${estimated_cost:,.0f} (at ${cost:.0f}/return)\n")

    lines.append("## Return rate by reason\n")
    lines.append("| Reason | Count | Share |")
    lines.append("|--------|------:|------:|")
    for reason, count in reason_counts.most_common():
        share = count / total_returns * 100 if total_returns else 0
        lines.append(f"| {reason} | {count:,} | {share:.1f}% |")
    lines.append("")

    lines.append(f"## Products above {threshold:.0f}% return rate\n")
    flagged = []
    for product, ret_count in product_returns.most_common():
        rate = ret_count / total_orders * 100
        if rate >= threshold:
            top_reason = product_reasons[product].most_common(1)[0][0] if product_reasons[product] else "unknown"
            flagged.append((product, ret_count, rate, top_reason))

    if flagged:
        lines.append("| Product | Returns | Return rate | Top reason |")
        lines.append("|---------|--------:|------------:|------------|")
        for product, ret_count, rate, top_reason in flagged:
            lines.append(f"| {product} | {ret_count:,} | {rate:.1f}% | {top_reason} |")
    else:
        lines.append(f"No products above {threshold:.0f}% return rate.")
    lines.append("")

    lines.append("## All products breakdown\n")
    lines.append("| Product | Returns | Top reason |")
    lines.append("|---------|--------:|------------|")
    for product, ret_count in product_returns.most_common():
        top_reason = product_reasons[product].most_common(1)[0][0] if product_reasons[product] else "unknown"
        lines.append(f"| {product} | {ret_count:,} | {top_reason} |")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a returns CSV and generate a return-rate report."
    )
    parser.add_argument("--in", dest="in_path", required=True, help="Path to returns CSV.")
    parser.add_argument("--threshold", type=float, default=10.0, help="Flag products above this return rate %%.")
    parser.add_argument("--total-orders", type=int, default=0, help="Total orders in period (for rate calc). If 0, uses return count as denominator.")
    parser.add_argument("--cost", type=float, default=DEFAULT_COST_PER_RETURN, help="Estimated cost per return in $.")
    parser.add_argument("--out", dest="out_path", default=None, help="Output file (default: stdout).")
    args = parser.parse_args()

    in_path = Path(args.in_path).expanduser()
    if not in_path.exists():
        print(f"File not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    rows = read_csv(in_path)
    total_orders = args.total_orders if args.total_orders > 0 else len(rows)
    report = analyze(rows, total_orders, args.threshold, args.cost)

    if args.out_path:
        out_path = Path(args.out_path).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written to {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
