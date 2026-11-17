#!/usr/bin/env python3
"""
pricing_strategies.py — Extended pricing methods for Tristan RFQ Overseer.

This module always anchors to the cost-plus baseline computed by
pricing_model.py (baseline transparency), then layers one additional
strategy on top for comparison. It never replaces the baseline — the
baseline is the cost floor and the reference point every other number is
measured against.

Strategies:
    cost-plus    Baseline only (delegates to pricing_model.py)
    market       Competitive / market-based pricing
    value        Value-based pricing
    volume       Tiered volume pricing
    target       Target costing / should-cost modeling
    escalation   Index-based / escalation pricing (long-term contracts)
    tco          Total cost of ownership (long-term contracts)
    report       Baseline + one strategy, combined client-facing summary

Usage examples:
    python pricing_strategies.py report RFQ-note.md --strategy market \
        --market-prices 17200 18500 19100

    python pricing_strategies.py escalation --base-price 50000 \
        --index-rate 0.035 --periods 5

    python pricing_strategies.py tco --acquisition 120000 \
        --annual-operating 8000 --annual-maintenance 3000 \
        --disposal 2000 --lifespan-years 10
"""

import argparse
import json
import re
import sys
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).parent))
from pricing_model import parse_line_items, compute_pricing, DEFAULT_MARGIN, DEFAULT_OVERHEAD  # noqa: E402


# ---------------------------------------------------------------------------
# Strategy 2: Competitive / market-based pricing
# ---------------------------------------------------------------------------
def market_based(baseline_total: float, market_prices: list, target_percentile: float = 0.5) -> dict:
    """Position the quote relative to observed competitor/market prices.

    target_percentile: 0.0 = match the lowest observed price,
                        1.0 = match the highest, 0.5 = market median-ish.
    Never suggests going below the cost-plus baseline — that would be
    selling at a loss regardless of what the market is doing.
    """
    if not market_prices:
        raise ValueError("At least one market price is required.")
    lo, hi = min(market_prices), max(market_prices)
    avg = round(mean(market_prices), 2)
    raw_suggested = lo + (hi - lo) * target_percentile
    suggested = round(max(raw_suggested, baseline_total), 2)
    below_cost_floor = suggested < baseline_total - 0.01
    return {
        "strategy": "market_based",
        "market_low": lo,
        "market_high": hi,
        "market_average": avg,
        "cost_floor": baseline_total,
        "suggested_price": suggested,
        "note": (
            "Suggested price was raised to the cost-plus floor to avoid "
            "pricing below cost." if raw_suggested < baseline_total else
            "Suggested price sits within the observed market range."
        ),
    }


# ---------------------------------------------------------------------------
# Strategy 3: Value-based pricing
# ---------------------------------------------------------------------------
def value_based(baseline_total: float, perceived_value: float, value_capture_rate: float = 0.3) -> dict:
    """Price toward a share of the value delivered to the client, never
    below the cost-plus floor."""
    if perceived_value <= 0:
        raise ValueError("perceived_value must be positive.")
    raw_suggested = round(perceived_value * value_capture_rate, 2)
    suggested = max(raw_suggested, baseline_total)
    return {
        "strategy": "value_based",
        "perceived_value": perceived_value,
        "value_capture_rate": value_capture_rate,
        "cost_floor": baseline_total,
        "suggested_price": round(suggested, 2),
    }


# ---------------------------------------------------------------------------
# Strategy 4: Tiered volume pricing
# ---------------------------------------------------------------------------
def tiered_volume(unit_cost: float, quantity: float, tiers: list) -> dict:
    """tiers: list of {"min_qty": int, "discount": float} sorted ascending
    by min_qty. discount is a fraction off unit_cost, e.g. 0.1 = 10% off."""
    applicable = [t for t in sorted(tiers, key=lambda t: t["min_qty"]) if quantity >= t["min_qty"]]
    tier = applicable[-1] if applicable else {"min_qty": 0, "discount": 0.0}
    discounted_unit_cost = round(unit_cost * (1 - tier["discount"]), 4)
    line_total = round(discounted_unit_cost * quantity, 2)
    return {
        "strategy": "tiered_volume",
        "quantity": quantity,
        "base_unit_cost": unit_cost,
        "tier_applied": tier,
        "discounted_unit_cost": discounted_unit_cost,
        "line_total": line_total,
        "all_tiers": tiers,
    }


# ---------------------------------------------------------------------------
# Strategy 5: Target costing / should-cost modeling
# ---------------------------------------------------------------------------
def target_costing(target_price: float, desired_margin: float, overhead_rate: float) -> dict:
    """Work backward from a market-driven target price to the maximum
    allowable cost base — useful for checking whether a supplier's quoted
    cost leaves room for a healthy margin, or whether the target is
    unrealistic given known cost structure."""
    if desired_margin >= 1:
        raise ValueError("desired_margin must be a fraction < 1, e.g. 0.18 for 18%.")
    max_cost_base = round(target_price / (1 + desired_margin), 2)
    max_subtotal = round(max_cost_base / (1 + overhead_rate), 2)
    return {
        "strategy": "target_costing",
        "target_price": target_price,
        "desired_margin": desired_margin,
        "overhead_rate": overhead_rate,
        "max_allowable_cost_base": max_cost_base,
        "max_allowable_subtotal": max_subtotal,
    }


# ---------------------------------------------------------------------------
# Strategy 6: Index-based / escalation pricing (long-term contracts)
# ---------------------------------------------------------------------------
def index_escalation(base_price: float, index_rate: float, periods: int, period_label: str = "year") -> dict:
    """Project a price forward across a multi-period contract using a
    fixed escalation rate (e.g. a materials index or CPI clause)."""
    schedule = []
    price = base_price
    for p in range(1, periods + 1):
        price = round(price * (1 + index_rate), 2)
        schedule.append({period_label: p, "escalated_price": price})
    return {
        "strategy": "index_escalation",
        "base_price": base_price,
        "index_rate": index_rate,
        "periods": periods,
        "period_label": period_label,
        "schedule": schedule,
        "note": "Intended for multi-year/long-term contracts with an escalation clause.",
    }


# ---------------------------------------------------------------------------
# Strategy 7: Total cost of ownership (long-term contracts)
# ---------------------------------------------------------------------------
def tco(acquisition_cost: float, annual_operating_cost: float, annual_maintenance_cost: float,
        disposal_cost: float, lifespan_years: int) -> dict:
    """Total cost of ownership over the asset's life — the number that
    matters for long-term comparisons, since the cheapest sticker price
    can be the most expensive option once operating cost is included."""
    lifetime_operating = round(annual_operating_cost * lifespan_years, 2)
    lifetime_maintenance = round(annual_maintenance_cost * lifespan_years, 2)
    total = round(acquisition_cost + lifetime_operating + lifetime_maintenance + disposal_cost, 2)
    annualized = round(total / lifespan_years, 2) if lifespan_years else None
    return {
        "strategy": "tco",
        "acquisition_cost": acquisition_cost,
        "lifetime_operating_cost": lifetime_operating,
        "lifetime_maintenance_cost": lifetime_maintenance,
        "disposal_cost": disposal_cost,
        "lifespan_years": lifespan_years,
        "total_cost_of_ownership": total,
        "annualized_cost": annualized,
        "note": "Intended for long-term/capital-equipment RFQs, not one-off purchases.",
    }


# ---------------------------------------------------------------------------
# Combined client-facing report: baseline + one strategy, side by side
# ---------------------------------------------------------------------------
def render_report_markdown(baseline: dict, strategy_result: dict) -> str:
    lines = [
        "## Pricing Strategy Comparison",
        "_Baseline is always cost-plus — shown for transparency alongside any other method used._",
        "",
        "### Baseline (Cost-Plus)",
        f"- Subtotal: {baseline['subtotal']:.2f}",
        f"- Overhead ({baseline['overhead_rate']*100:.1f}%): {baseline['overhead_amount']:.2f}",
        f"- Margin ({baseline['margin_rate']*100:.1f}%): {baseline['margin_amount']:.2f}",
        f"- **Baseline total (cost floor): {baseline['total']:.2f}**",
        "",
        f"### {strategy_result['strategy'].replace('_', ' ').title()}",
    ]
    for k, v in strategy_result.items():
        if k in ("strategy", "note", "schedule", "all_tiers"):
            continue
        lines.append(f"- {k.replace('_', ' ').title()}: {v}")
    if "note" in strategy_result:
        lines.append(f"\n> {strategy_result['note']}")
    if "schedule" in strategy_result:
        lines.append("\n| Period | Escalated Price |\n|---|---|")
        for row in strategy_result["schedule"]:
            period_key = strategy_result.get("period_label", "period")
            lines.append(f"| {row[period_key]} | {row['escalated_price']:.2f} |")
    return "\n".join(lines)


def write_back(note_path: Path, section_markdown: str) -> None:
    note_text = note_path.read_text(encoding="utf-8")
    section_re = re.compile(r"## Pricing Strategy Comparison\n.*?(?=\n## |\Z)", re.DOTALL)
    if section_re.search(note_text):
        updated = section_re.sub(section_markdown.rstrip("\n") + "\n", note_text, count=1)
    else:
        updated = note_text.rstrip("\n") + "\n\n" + section_markdown + "\n"
    note_path.write_text(updated, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Extended pricing strategies for Tristan RFQ Overseer.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_report = sub.add_parser("report", help="Baseline + one strategy, combined for client-facing use.")
    p_report.add_argument("note", type=Path)
    p_report.add_argument("--strategy", required=True, choices=["market", "value", "target", "escalation", "tco"])
    p_report.add_argument("--margin", type=float, default=DEFAULT_MARGIN)
    p_report.add_argument("--overhead", type=float, default=DEFAULT_OVERHEAD)
    p_report.add_argument("--market-prices", type=float, nargs="+")
    p_report.add_argument("--target-percentile", type=float, default=0.5)
    p_report.add_argument("--perceived-value", type=float)
    p_report.add_argument("--value-capture-rate", type=float, default=0.3)
    p_report.add_argument("--target-price", type=float)
    p_report.add_argument("--desired-margin", type=float)
    p_report.add_argument("--index-rate", type=float)
    p_report.add_argument("--periods", type=int)
    p_report.add_argument("--acquisition", type=float)
    p_report.add_argument("--annual-operating", type=float)
    p_report.add_argument("--annual-maintenance", type=float)
    p_report.add_argument("--disposal", type=float)
    p_report.add_argument("--lifespan-years", type=int)
    p_report.add_argument("--write", action="store_true")

    p_market = sub.add_parser("market", help="Competitive / market-based pricing.")
    p_market.add_argument("--baseline-total", type=float, required=True)
    p_market.add_argument("--market-prices", type=float, nargs="+", required=True)
    p_market.add_argument("--target-percentile", type=float, default=0.5)

    p_value = sub.add_parser("value", help="Value-based pricing.")
    p_value.add_argument("--baseline-total", type=float, required=True)
    p_value.add_argument("--perceived-value", type=float, required=True)
    p_value.add_argument("--value-capture-rate", type=float, default=0.3)

    p_volume = sub.add_parser("volume", help="Tiered volume pricing for a single line item.")
    p_volume.add_argument("--unit-cost", type=float, required=True)
    p_volume.add_argument("--quantity", type=float, required=True)
    p_volume.add_argument("--tiers-json", type=str, required=True,
                           help='e.g. \'[{"min_qty":100,"discount":0.05},{"min_qty":500,"discount":0.12}]\'')

    p_target = sub.add_parser("target", help="Target costing / should-cost modeling.")
    p_target.add_argument("--target-price", type=float, required=True)
    p_target.add_argument("--desired-margin", type=float, required=True)
    p_target.add_argument("--overhead-rate", type=float, default=DEFAULT_OVERHEAD)

    p_esc = sub.add_parser("escalation", help="Index-based / escalation pricing.")
    p_esc.add_argument("--base-price", type=float, required=True)
    p_esc.add_argument("--index-rate", type=float, required=True)
    p_esc.add_argument("--periods", type=int, required=True)
    p_esc.add_argument("--period-label", type=str, default="year")

    p_tco = sub.add_parser("tco", help="Total cost of ownership.")
    p_tco.add_argument("--acquisition", type=float, required=True)
    p_tco.add_argument("--annual-operating", type=float, required=True)
    p_tco.add_argument("--annual-maintenance", type=float, required=True)
    p_tco.add_argument("--disposal", type=float, default=0.0)
    p_tco.add_argument("--lifespan-years", type=int, required=True)

    args = parser.parse_args()

    if args.command == "market":
        print(json.dumps(market_based(args.baseline_total, args.market_prices, args.target_percentile), indent=2))
    elif args.command == "value":
        print(json.dumps(value_based(args.baseline_total, args.perceived_value, args.value_capture_rate), indent=2))
    elif args.command == "volume":
        tiers = json.loads(args.tiers_json)
        print(json.dumps(tiered_volume(args.unit_cost, args.quantity, tiers), indent=2))
    elif args.command == "target":
        print(json.dumps(target_costing(args.target_price, args.desired_margin, args.overhead_rate), indent=2))
    elif args.command == "escalation":
        print(json.dumps(index_escalation(args.base_price, args.index_rate, args.periods, args.period_label), indent=2))
    elif args.command == "tco":
        print(json.dumps(
            tco(args.acquisition, args.annual_operating, args.annual_maintenance, args.disposal, args.lifespan_years),
            indent=2,
        ))
    elif args.command == "report":
        if not args.note.exists():
            print(f"Error: note not found at {args.note}", file=sys.stderr)
            sys.exit(1)
        note_text = args.note.read_text(encoding="utf-8")
        items = parse_line_items(note_text)
        if not items:
            print("No valid line items found in the note.", file=sys.stderr)
            sys.exit(1)
        baseline = compute_pricing(items, args.margin, args.overhead)

        if args.strategy == "market":
            if not args.market_prices:
                sys.exit("--market-prices is required for --strategy market")
            result = market_based(baseline["total"], args.market_prices, args.target_percentile)
        elif args.strategy == "value":
            if not args.perceived_value:
                sys.exit("--perceived-value is required for --strategy value")
            result = value_based(baseline["total"], args.perceived_value, args.value_capture_rate)
        elif args.strategy == "target":
            if not args.target_price or args.desired_margin is None:
                sys.exit("--target-price and --desired-margin are required for --strategy target")
            result = target_costing(args.target_price, args.desired_margin, args.overhead)
        elif args.strategy == "escalation":
            if not args.index_rate or not args.periods:
                sys.exit("--index-rate and --periods are required for --strategy escalation")
            result = index_escalation(baseline["total"], args.index_rate, args.periods)
        elif args.strategy == "tco":
            required = [args.acquisition, args.annual_operating, args.annual_maintenance, args.lifespan_years]
            if any(v is None for v in required):
                sys.exit("--acquisition, --annual-operating, --annual-maintenance, --lifespan-years are required for --strategy tco")
            result = tco(args.acquisition, args.annual_operating, args.annual_maintenance,
                         args.disposal or 0.0, args.lifespan_years)

        report_md = render_report_markdown(baseline, result)
        print(report_md)
        if args.write:
            write_back(args.note, report_md)
            print(f"\nWritten to {args.note}", file=sys.stderr)


if __name__ == "__main__":
    main()
