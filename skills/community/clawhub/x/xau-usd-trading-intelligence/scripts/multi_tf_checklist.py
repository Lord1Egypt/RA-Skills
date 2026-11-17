#!/usr/bin/env python3
"""xau-usd-trading-intelligence: multi-timeframe (HTF/ITF/LTF) checklist printer.

Reads manual inputs (no API, no network) and prints a structured confluence
checklist plus a simple signal-quality score (0-100) aligned with the skill's
internal decision framework (Structure + Liquidity + Momentum + Volatility +
Macro + Session + Correlation + R:R).

Usage (flags take 0/1 or true/false):
  python3 multi_tf_checklist.py \
    --htf "D bullish, key 2300/2350" \
    --itf "H1 pullback to OB" \
    --ltf "M5 BoS + sweep" \
    --structure 1 --liquidity 1 --momentum 1 --volatility 0 \
    --macro 1 --session 1 --correlation 1 --rr 1

Weights (sum 100): structure 20, momentum 15, liquidity 15, macro 15,
volatility 10, session 10, correlation 5, rr 10.
Score >=70 -> trade candidate; >=90 A+; <60 NO TRADE.
"""
import argparse
import sys

WEIGHTS = {
    "structure": 20, "momentum": 15, "liquidity": 15, "macro": 15,
    "volatility": 10, "session": 10, "correlation": 5, "rr": 10,
}


def truthy(v):
    return str(v).lower() in ("1", "true", "yes", "y", "on")


def main():
    p = argparse.ArgumentParser(description="XAU/USD multi-TF checklist")
    p.add_argument("--htf", default="", help="HTF context (W/D/4H bias + key levels)")
    p.add_argument("--itf", default="", help="ITF setup (1H/15M pullback to value)")
    p.add_argument("--ltf", default="", help="LTF trigger (5M/1M BoS/CHoCH/sweep)")
    for k in WEIGHTS:
        p.add_argument(f"--{k}", default="0", help=f"{k} present? 0/1")
    args = p.parse_args()

    score = 0
    print("XAU/USD MULTI-TIMEFRAME CHECKLIST")
    print("-" * 40)
    print(f"HTF : {args.htf or '(empty)'}")
    print(f"ITF : {args.itf or '(empty)'}")
    print(f"LTF : {args.ltf or '(empty)'}")
    print("-" * 40)
    print("CONFLUENCE:")
    for k, w in WEIGHTS.items():
        on = truthy(getattr(args, k))
        score += w if on else 0
        mark = "YES" if on else "no "
        print(f"  [{mark}] {k:<11} (+{w})")
    print("-" * 40)
    print(f"SIGNAL QUALITY SCORE: {score}/100")
    if score >= 90:
        verdict = "A+ candidate"
    elif score >= 70:
        verdict = "Trade candidate (plan SL/TP, journal before entry)"
    elif score >= 60:
        verdict = "C - weak; require stronger confluence"
    else:
        verdict = "NO TRADE / LOW QUALITY"
    print(f"VERDICT: {verdict}")
    print("-" * 40)
    print("Note: data-driven confirmation still required before any entry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
