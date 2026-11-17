#!/usr/bin/env python3
"""
compare_quotes.py — Stage 4 supplier quote ranking for Tristan RFQ Overseer.

Reads one or more supplier quote JSON files and ranks them by a weighted
score of price, lead time, and certificate status. Designed to be pointed at
a directory of per-supplier quote files collected during the tracking stage.

Each input JSON file should look like:
    {
        "supplier": "Acme Fabrication",
        "price": 18250.00,
        "lead_time_days": 21,
        "cert_status": "valid",       # valid | expiring_soon | expired | unknown
        "notes": "optional free text"
    }

For long-term / capital-equipment RFQs, add TCO fields and pass --tco to
rank on total cost of ownership instead of sticker price — this is what
lets you show a client that the cheapest quote isn't always the cheapest
option over the life of the contract:
    {
        "supplier": "Acme Fabrication",
        "price": 120000.00,
        "lead_time_days": 45,
        "cert_status": "valid",
        "annual_operating_cost": 8000.00,
        "annual_maintenance_cost": 3000.00,
        "disposal_cost": 2000.00,
        "lifespan_years": 10
    }

Usage:
    python compare_quotes.py <path/to/quotes_dir> [--weight-price 0.5]
                                                    [--weight-lead 0.3]
                                                    [--weight-cert 0.2]
                                                    [--tco]
                                                    [--markdown]
"""

import argparse
import json
import sys
from pathlib import Path

CERT_SCORE = {
    "valid": 1.0,
    "expiring_soon": 0.6,
    "expired": 0.0,
    "unknown": 0.3,
}


def load_quotes(quotes_dir: Path):
    quotes = []
    for path in sorted(quotes_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"Warning: skipping unparseable file {path}", file=sys.stderr)
            continue
        required = {"supplier", "price", "lead_time_days"}
        if not required.issubset(data):
            print(f"Warning: skipping {path}, missing fields {required - set(data)}", file=sys.stderr)
            continue
        data.setdefault("cert_status", "unknown")
        data["_source_file"] = path.name
        quotes.append(data)
    return quotes


def normalize(values, lower_is_better=True):
    """Min-max normalize to a 0-1 'goodness' score."""
    if not values:
        return {}
    lo, hi = min(values), max(values)
    if hi == lo:
        return {v: 1.0 for v in values}
    scores = {}
    for v in values:
        frac = (v - lo) / (hi - lo)
        scores[v] = (1 - frac) if lower_is_better else frac
    return scores


def effective_price(q: dict, use_tco: bool) -> float:
    """Sticker price, or total cost of ownership if --tco is set and the
    quote has TCO fields. Falls back to sticker price with a warning if
    TCO fields are missing, so a mixed set of files doesn't silently rank
    wrong."""
    if not use_tco:
        return q["price"]
    required = {"annual_operating_cost", "annual_maintenance_cost", "lifespan_years"}
    if not required.issubset(q):
        print(f"Warning: {q.get('_source_file', q.get('supplier'))} missing TCO fields "
              f"{required - set(q)} — falling back to sticker price for ranking.", file=sys.stderr)
        return q["price"]
    lifespan = q["lifespan_years"]
    total = (
        q["price"]
        + q["annual_operating_cost"] * lifespan
        + q["annual_maintenance_cost"] * lifespan
        + q.get("disposal_cost", 0.0)
    )
    return round(total, 2)


def rank_quotes(quotes, w_price, w_lead, w_cert, use_tco=False):
    for q in quotes:
        q["_effective_price"] = effective_price(q, use_tco)

    effective_prices = [q["_effective_price"] for q in quotes]
    leads = [q["lead_time_days"] for q in quotes]
    price_scores = normalize(effective_prices, lower_is_better=True)
    lead_scores = normalize(leads, lower_is_better=True)

    ranked = []
    for q in quotes:
        cert_score = CERT_SCORE.get(q.get("cert_status", "unknown"), 0.3)
        score = (
            w_price * price_scores[q["_effective_price"]]
            + w_lead * lead_scores[q["lead_time_days"]]
            + w_cert * cert_score
        )
        ranked.append({**q, "score": round(score, 4)})

    ranked.sort(key=lambda q: q["score"], reverse=True)
    for i, q in enumerate(ranked, start=1):
        q["rank"] = i
    return ranked


def render_markdown(ranked, use_tco=False):
    if use_tco:
        lines = [
            "| Supplier | Sticker Price | Total Cost of Ownership | Lead Time | Cert Status | Rank |",
            "|---|---|---|---|---|---|",
        ]
        for q in ranked:
            lines.append(
                f"| {q['supplier']} | {q['price']:.2f} | {q['_effective_price']:.2f} | "
                f"{q['lead_time_days']}d | {q.get('cert_status', 'unknown')} | {q['rank']} |"
            )
        lines.append("\n_Ranked by total cost of ownership, not sticker price — "
                      "this is the number to show a client who assumes cheapest quote wins._")
    else:
        lines = [
            "| Supplier | Quoted Price | Lead Time | Cert Status | Rank |",
            "|---|---|---|---|---|",
        ]
        for q in ranked:
            lines.append(
                f"| {q['supplier']} | {q['price']:.2f} | {q['lead_time_days']}d | "
                f"{q.get('cert_status', 'unknown')} | {q['rank']} |"
            )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Rank supplier quotes for an RFQ.")
    parser.add_argument("quotes_dir", type=Path, help="Directory containing per-supplier quote JSON files")
    parser.add_argument("--weight-price", type=float, default=0.5)
    parser.add_argument("--weight-lead", type=float, default=0.3)
    parser.add_argument("--weight-cert", type=float, default=0.2)
    parser.add_argument("--tco", action="store_true",
                         help="Rank by total cost of ownership instead of sticker price (long-term/capital RFQs)")
    parser.add_argument("--markdown", action="store_true", help="Print a markdown table instead of JSON")
    args = parser.parse_args()

    if not args.quotes_dir.exists() or not args.quotes_dir.is_dir():
        print(f"Error: quotes directory not found at {args.quotes_dir}", file=sys.stderr)
        sys.exit(1)

    weight_sum = args.weight_price + args.weight_lead + args.weight_cert
    if abs(weight_sum - 1.0) > 1e-6:
        print(f"Warning: weights sum to {weight_sum}, not 1.0 — scores will be scaled accordingly.", file=sys.stderr)

    quotes = load_quotes(args.quotes_dir)
    if not quotes:
        print("No valid supplier quote files found.", file=sys.stderr)
        sys.exit(1)

    ranked = rank_quotes(quotes, args.weight_price, args.weight_lead, args.weight_cert, use_tco=args.tco)

    if args.markdown:
        print(render_markdown(ranked, use_tco=args.tco))
    else:
        print(json.dumps(ranked, indent=2))


if __name__ == "__main__":
    main()
