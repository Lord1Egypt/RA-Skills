#!/usr/bin/env python3
"""Analyze US stock financial indicators from CSV/JSON data.

Usage:
  python3 analyze_financials.py <input_file> [--format csv|json] [--output json|markdown] [--index sp500|nasdaq|all]

Input file must contain columns (CSV) or keys (JSON):
  ticker, name, sector, market_cap, pe_ratio, pb_ratio, roe, debt_to_equity, revenue_growth, net_margin, current_ratio, dividend_yield

Output: financial health scores, sector rankings, red flags, and summary.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

WEIGHTS = {
    "pe_ratio": 0.15,
    "pb_ratio": 0.10,
    "roe": 0.20,
    "debt_to_equity": 0.15,
    "revenue_growth": 0.15,
    "net_margin": 0.15,
    "current_ratio": 0.05,
    "dividend_yield": 0.05,
}

THRESHOLDS = {
    "pe_ratio": {"good": 20, "warn": 35},
    "pb_ratio": {"good": 3, "warn": 6},
    "roe": {"good": 0.15, "warn": 0.08},
    "debt_to_equity": {"good": 0.5, "warn": 1.5},
    "revenue_growth": {"good": 0.10, "warn": 0.03},
    "net_margin": {"good": 0.15, "warn": 0.05},
    "current_ratio": {"good": 2.0, "warn": 1.0},
    "dividend_yield": {"good": 0.02, "warn": 0.005},
}

# Higher is better for: roe, revenue_growth, net_margin, current_ratio, dividend_yield
# Lower is better for: pe_ratio, pb_ratio, debt_to_equity
LOWER_IS_BETTER = {"pe_ratio", "pb_ratio", "debt_to_equity"}


def score_metric(value, metric):
    t = THRESHOLDS[metric]
    if metric in LOWER_IS_BETTER:
        if value <= t["good"]:
            return 100
        elif value <= t["warn"]:
            return max(0, 100 - (value - t["good"]) / (t["warn"] - t["good"]) * 60)
        else:
            return max(0, 40 - (value - t["warn"]) / t["warn"] * 40)
    else:
        if value >= t["good"]:
            return 100
        elif value >= t["warn"]:
            return max(0, 40 + (value - t["warn"]) / (t["good"] - t["warn"]) * 60)
        else:
            return max(0, value / t["warn"] * 40)


def _num(row, key, default=0):
    v = row.get(key, default)
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def red_flags(row):
    flags = []
    if _num(row, "pe_ratio") > THRESHOLDS["pe_ratio"]["warn"]:
        flags.append(f"PE ratio {_num(row, 'pe_ratio'):.1f} > {THRESHOLDS['pe_ratio']['warn']}")
    if _num(row, "debt_to_equity") > THRESHOLDS["debt_to_equity"]["warn"]:
        flags.append(f"Debt/Equity {_num(row, 'debt_to_equity'):.2f} > {THRESHOLDS['debt_to_equity']['warn']}")
    if 0 < _num(row, "roe") < THRESHOLDS["roe"]["warn"]:
        flags.append(f"Low ROE {_num(row, 'roe'):.2%}")
    if _num(row, "revenue_growth") < 0:
        flags.append(f"Negative revenue growth {_num(row, 'revenue_growth'):.2%}")
    if _num(row, "current_ratio") < THRESHOLDS["current_ratio"]["warn"]:
        flags.append(f"Current ratio {_num(row, 'current_ratio'):.2f} < {THRESHOLDS['current_ratio']['warn']}")
    return flags


def analyze(rows, index_filter=None):
    results = []
    for row in rows:
        if index_filter and index_filter != "all":
            idx = row.get("index", "").lower()
            if index_filter == "sp500" and idx != "sp500":
                continue
            if index_filter == "nasdaq" and idx != "nasdaq":
                continue

        scores = {}
        for metric, weight in WEIGHTS.items():
            val = row.get(metric)
            if val is None or val == "":
                scores[metric] = None
                continue
            val = _num(row, metric)
            scores[metric] = score_metric(val, metric) * weight

        total = sum(s for s in scores.values() if s is not None)
        max_possible = sum(WEIGHTS[m] * 100 for m, s in scores.items() if s is not None)
        normalized = (total / max_possible * 100) if max_possible > 0 else 0

        results.append({
            "ticker": row.get("ticker", ""),
            "name": row.get("name", ""),
            "sector": row.get("sector", ""),
            "index": row.get("index", ""),
            "market_cap": row.get("market_cap", ""),
            "overall_score": round(normalized, 1),
            "metric_scores": {k: round(v, 1) if v is not None else None for k, v in scores.items()},
            "red_flags": red_flags(row),
        })

    results.sort(key=lambda x: x["overall_score"], reverse=True)
    return results


def sector_rankings(results):
    sectors = {}
    for r in results:
        s = r["sector"]
        sectors.setdefault(s, []).append(r["overall_score"])
    return {s: round(sum(v) / len(v), 1) for s, v in sorted(sectors.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)}


def to_markdown(results, sectors):
    lines = ["# Financial Analysis Report\n"]
    lines.append("## Sector Rankings\n")
    for s, avg in sectors.items():
        bar = "█" * int(avg / 5)
        lines.append(f"| {s} | {avg} | {bar} |")
    lines.append("\n## Top 10 Stocks\n")
    lines.append("| Rank | Ticker | Name | Score | Red Flags |")
    lines.append("|------|--------|------|-------|-----------|")
    for i, r in enumerate(results[:10], 1):
        flags = "; ".join(r["red_flags"]) if r["red_flags"] else "—"
        lines.append(f"| {i} | {r['ticker']} | {r['name']} | {r['overall_score']} | {flags} |")
    lines.append("\n## Bottom 5 Stocks\n")
    lines.append("| Rank | Ticker | Name | Score | Red Flags |")
    lines.append("|------|--------|------|-------|-----------|")
    for i, r in enumerate(results[-5:], max(1, len(results) - 4)):
        flags = "; ".join(r["red_flags"]) if r["red_flags"] else "—"
        lines.append(f"| {i} | {r['ticker']} | {r['name']} | {r['overall_score']} | {flags} |")
    high_risk = [r for r in results if len(r["red_flags"]) >= 3]
    if high_risk:
        lines.append(f"\n## ⚠️ High-Risk Stocks ({len(high_risk)} with ≥3 red flags)\n")
        for r in high_risk[:20]:
            lines.append(f"- **{r['ticker']}** ({r['name']}): " + "; ".join(r["red_flags"]))
    return "\n".join(lines)


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def main():
    parser = argparse.ArgumentParser(description="Analyze US stock financial indicators")
    parser.add_argument("input", help="Input file path (CSV or JSON)")
    parser.add_argument("--format", choices=["csv", "json"], default=None, help="Input format (auto-detected)")
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--index", choices=["sp500", "nasdaq", "all"], default="all")
    args = parser.parse_args()

    fmt = args.format or ("json" if args.input.endswith(".json") else "csv")
    rows = load_json(args.input) if fmt == "json" else load_csv(args.input)

    if not rows:
        print("No data found.", file=sys.stderr)
        sys.exit(1)

    results = analyze(rows, args.index)
    sectors = sector_rankings(results)

    if args.output == "json":
        print(json.dumps({"results": results, "sector_rankings": sectors}, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(results, sectors))


if __name__ == "__main__":
    main()
