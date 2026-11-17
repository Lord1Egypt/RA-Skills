#!/usr/bin/env python3
"""
forecast_cli — single-shot options forecast + play recommender.

Usage:
  python3 forecast_cli.py --ticker MU
  python3 forecast_cli.py --ticker MU --expiry 2026-07-27
  python3 forecast_cli.py --ticker MU --expiry 2026-07-27 --top-n 5

Outputs to stdout:
  1. Forecast header (spot, forward, ATM IV, expected move, DTE)
  2. Risk-neutral median + CI bands (50/80/95%)
  3. Directional read (Q(close > spot) + RN direction)
  4. Top-N options plays with strikes, prices, PoP, R/R, breakevens

Optional flags:
  --json                 Emit machine-readable JSON instead of text
  --out PATH             Also write the JSON to PATH
  --dividend-yield Q     Override continuous dividend yield (default 0)
  --rate R               Override risk-free rate (default 0.050 / env RISK_FREE_RATE)

Requires:
  LONDON_STRATEGIC_EDGE_API_KEY in environment (.env auto-loaded)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from dotenv import load_dotenv

load_dotenv()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="forecast_cli.py",
        description="Forecast stock close at expiration + options play recommendations.",
        epilog=(
            "Examples:\n"
            "  python3 scripts/forecast_cli.py --ticker MU --expiry 2026-07-31\n"
            "  python3 scripts/forecast_cli.py --ticker MU                          # nearest expiry\n"
            "  python3 scripts/forecast_cli.py --ticker AAPL --rate 0.053 --dividend-yield 0.005\n"
            "  python3 scripts/forecast_cli.py --ticker MU --expiry 2026-09-18 --json --out /tmp/mu.json\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--ticker", required=True, metavar="TICKER",
                        help="Stock symbol, e.g. MU, AAPL, NBIS")
    parser.add_argument("--expiry", default=None, metavar="YYYY-MM-DD",
                        help="Expiration date. Default: nearest from flow.")
    parser.add_argument("--top-n", type=int, default=4, metavar="N",
                        help="Number of options plays to surface (default 4)")
    parser.add_argument("--flow-limit", type=int, default=5000, metavar="N",
                        help="Max flow prints to pull from LSE (default 5000)")
    parser.add_argument("--dividend-yield", type=float, default=None, metavar="Q",
                        help="Continuous dividend yield q (default 0)")
    parser.add_argument("--rate", type=float, default=None, metavar="R",
                        help="Risk-free rate r (default 0.050 or env RISK_FREE_RATE)")
    parser.add_argument("--realized-variance", type=float, default=None, metavar="V",
                        help="Realized variance for VRP diagnostic (optional)")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON instead of text")
    parser.add_argument("--out", default=None, metavar="PATH",
                        help="Also write JSON to this path")
    args = parser.parse_args(argv)

    symbol = args.ticker.upper()
    expiry_display = args.expiry or "(nearest)"

    # Lazy imports — keeps --help fast and isolates import errors
    try:
        from lse_options import LSEClient, _latest_spot, LSEError
        from expiration_model import forecast_expiration
        from recommend_plays import recommend_plays
    except ImportError as e:
        print(f"Missing dependency: {e}", file=sys.stderr)
        print("Run: pip install scipy numpy python-dotenv plotly certifi",
              file=sys.stderr)
        return 2

    if not os.environ.get("LONDON_STRATEGIC_EDGE_API_KEY"):
        print("LONDON_STRATEGIC_EDGE_API_KEY not set. Put it in .env or export it.",
              file=sys.stderr)
        return 2

    try:
        client = LSEClient()
        flow = client.options_flow(symbol, limit=args.flow_limit)
    except LSEError as e:
        print(f"LSE API error: {e}", file=sys.stderr)
        return 3

    if not flow:
        print(f"No flow data for {symbol}", file=sys.stderr)
        return 4

    try:
        spot = _latest_spot(flow)
    except ValueError as e:
        print(f"Could not extract spot: {e}", file=sys.stderr)
        return 5

    try:
        forecast = forecast_expiration(
            flow, spot,
            target_expiry=args.expiry,
            r=args.rate,
            q=args.dividend_yield,
            realized_variance=args.realized_variance,
        )
    except Exception as e:
        print(f"Forecast failed: {e}", file=sys.stderr)
        return 6

    plays = recommend_plays(forecast, top_n=args.top_n)

    input_echo = {
        "ticker": symbol,
        "expiry_requested": expiry_display,
        "expiry_resolved": forecast.expiry,
        "dte": forecast.dte,
        "top_n": args.top_n,
        "rate": args.rate if args.rate is not None else float(os.environ.get("RISK_FREE_RATE", "0.050")),
        "dividend_yield": args.dividend_yield if args.dividend_yield is not None else 0.0,
    }

    payload = _serialize(symbol, forecast, plays)
    payload["input"] = input_echo

    if args.json:
        out = json.dumps(payload, indent=2, default=str)
        print(out)
        if args.out:
            with open(args.out, "w") as f:
                f.write(out)
    else:
        _print_input_banner(input_echo)
        report = _format_text_report(symbol, forecast, plays)
        print(report)
        if args.out:
            with open(args.out, "w") as f:
                json.dump(payload, f, indent=2, default=str)

    return 0


def _print_input_banner(input_echo: dict) -> None:
    """Show the expected input template + what was actually parsed."""
    bar = "─" * 72
    print(bar)
    print("  Usage:  forecast_cli.py --ticker <TICKER> --expiry <YYYY-MM-DD>")
    print("          e.g.  --ticker MU --expiry 2026-07-31")
    print(bar)
    print(f"  Input received:")
    print(f"    ticker:           {input_echo['ticker']}")
    print(f"    expiry requested: {input_echo['expiry_requested']}")
    print(f"    expiry resolved:  {input_echo['expiry_resolved']}  ({input_echo['dte']}d)")
    print(f"    top_n:            {input_echo['top_n']}")
    print(f"    rate r:           {input_echo['rate']:.2%}")
    print(f"    dividend q:       {input_echo['dividend_yield']:.2%}")
    print(bar)
    print()


def _serialize(symbol: str, forecast, plays) -> dict:
    return {
        "symbol": symbol,
        "spot": forecast.spot,
        "expiry": forecast.expiry,
        "dte": forecast.dte,
        "forward_price": forecast.forward_price,
        "r": forecast.r,
        "q": forecast.q,
        "atm_iv": forecast.atm_iv,
        "expected_move_1sigma": forecast.expected_move_1sigma,
        "median": forecast.median,
        "mean": forecast.mean,
        "prob_above_spot": forecast.prob_above_spot,
        "rn_direction": forecast.rn_direction,
        "ci_50": list(forecast.ci_50),
        "ci_80": list(forecast.ci_80),
        "ci_95": list(forecast.ci_95),
        "skew_25d_rr": forecast.skew,
        "arb_check": forecast.arb_check,
        "vrp_proxy": forecast.vrp_proxy,
        "plays": [
            {
                "name": p.name,
                "bias": p.bias,
                "structure": p.structure,
                "net_debit": p.net_debit,
                "max_profit": p.max_profit,
                "max_loss": p.max_loss,
                "breakevens": p.breakevens,
                "pop_risk_neutral": p.pop_risk_neutral,
                "reward_to_risk": p.reward_to_risk,
                "legs": [
                    {"action": l.action, "type": l.type,
                     "strike": l.strike, "price": l.approx_price, "qty": l.qty}
                    for l in p.legs
                ],
                "rationale": p.rationale,
            }
            for p in plays
        ],
    }


def _format_text_report(symbol: str, forecast, plays) -> str:
    dirs = {1: "BULLISH", -1: "BEARISH", 0: "NEUTRAL"}
    rn_label = dirs[forecast.rn_direction]
    pct_lo_50 = (forecast.ci_50[0] - forecast.spot) / forecast.spot
    pct_hi_50 = (forecast.ci_50[1] - forecast.spot) / forecast.spot
    pct_lo_80 = (forecast.ci_80[0] - forecast.spot) / forecast.spot
    pct_hi_80 = (forecast.ci_80[1] - forecast.spot) / forecast.spot
    pct_lo_95 = (forecast.ci_95[0] - forecast.spot) / forecast.spot
    pct_hi_95 = (forecast.ci_95[1] - forecast.spot) / forecast.spot

    lines = [
        "=" * 72,
        f"  {symbol} — Expiration Close Forecast ({forecast.expiry}, {forecast.dte}d)",
        "=" * 72,
        "",
        f"  Spot:       ${forecast.spot:>9,.2f}",
        f"  Forward:    ${forecast.forward_price:>9,.2f}  (r={forecast.r:.2%}, q={forecast.q:.2%})",
        f"  ATM IV:     {forecast.atm_iv:>10.1%}",
        f"  1σ move:    ${forecast.expected_move_1sigma:>9,.2f} ({forecast.expected_move_1sigma/forecast.spot:.1%})",
        f"  Skew 25ΔRR: {forecast.skew:>+10.4f}",
        "",
        "-" * 72,
        "  RISK-NEUTRAL CLOSE FORECAST  (market-implied, NOT real-world)",
        "-" * 72,
        "",
        f"  Median close:  ${forecast.median:>9,.2f}   "
        f"({(forecast.median - forecast.spot) / forecast.spot:+.1%} vs spot)",
        f"  Mean close:    ${forecast.mean:>9,.2f}   "
        f"(forward ${forecast.forward_price:,.2f}; μ/F={forecast.arb_check.get('mean_to_forward', 0):.3f})",
        f"  Q(close > spot) = {forecast.prob_above_spot:.1%}   →  {rn_label}",
        "",
        "  Confidence Intervals (risk-neutral quantiles, ±% vs spot):",
        f"    50% CI:  ${forecast.ci_50[0]:>8,.0f}  to  ${forecast.ci_50[1]:>8,.0f}   "
        f"({pct_lo_50:+.1%} / {pct_hi_50:+.1%})",
        f"    80% CI:  ${forecast.ci_80[0]:>8,.0f}  to  ${forecast.ci_80[1]:>8,.0f}   "
        f"({pct_lo_80:+.1%} / {pct_hi_80:+.1%})",
        f"    95% CI:  ${forecast.ci_95[0]:>8,.0f}  to  ${forecast.ci_95[1]:>8,.0f}   "
        f"({pct_lo_95:+.1%} / {pct_hi_95:+.1%})",
        "",
        "-" * 72,
        f"  RECOMMENDED OPTIONS PLAYS  (top {len(plays)}, ranked by PoP × R/R)",
        "-" * 72,
        "",
    ]

    for i, p in enumerate(plays, 1):
        lines.append(f"  Play #{i}:")
        lines.append(p.format())
        lines.append("")

    lines.extend([
        "-" * 72,
        "  NOTES",
        "-" * 72,
        "  • All probabilities are RISK-NEUTRAL (market-implied). Due to the variance",
        "    risk premium, real-world PoP is typically HIGHER for short-vol plays",
        "    (credit spreads, condors) and LOWER for long-vol plays (straddles).",
        "  • Approximate prices use ATM IV at forecast grid strikes; verify against",
        "    live quotes before execution.",
        "  • CI widths can be narrow if the smile fit is sparse — sanity-check the",
        f"    no-arb status (currently: {forecast.arb_check.get('status', 'n/a')}).",
        "  • This is research tooling, not investment advice.",
        "=" * 72,
    ])
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
