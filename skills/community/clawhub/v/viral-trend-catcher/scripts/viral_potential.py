#!/usr/bin/env python3
"""
Score a product's viral potential across five weighted dimensions
and output a formatted go/no-go recommendation.

Weights:
  visual hook   30%
  impulse price 25%
  shareability  25%
  trend stage   10%
  IP risk       10%
"""
from __future__ import annotations

import argparse
import sys

TREND_STAGE_SCORES = {
    "rising": 5,
    "peak": 3,
    "declining": 1,
}

IP_RISK_SCORES = {
    "low": 5,
    "medium": 3,
    "high": 1,
}

DIMENSIONS = [
    ("visual_hook",   "Visual Hook (3-second stop-scroll power)",  30),
    ("impulse_price", "Impulse Price (buy-without-thinking range)", 25),
    ("shareability",  "Shareability (will buyers film & post?)",    25),
    ("trend_stage",   "Trend Stage (rising → peak → declining)",    10),
    ("ip_risk",       "IP Risk (low is good, high is dangerous)",   10),
]


def score_viral_potential(
    visual_hook: int,
    impulse_price: int,
    shareability: int,
    trend_stage: str,
    ip_risk: str,
) -> tuple[int, str, str]:
    """
    Calculate weighted viral score (0–100) and return
    (score, verdict, formatted_report).
    """
    trend_score = TREND_STAGE_SCORES.get(trend_stage)
    if trend_score is None:
        raise ValueError(f"trend-stage must be one of {list(TREND_STAGE_SCORES)}")
    ip_score = IP_RISK_SCORES.get(ip_risk)
    if ip_score is None:
        raise ValueError(f"ip-risk must be one of {list(IP_RISK_SCORES)}")

    raw_scores = [visual_hook, impulse_price, shareability]
    if not all(1 <= s <= 5 for s in raw_scores):
        raise ValueError("visual-hook, impulse-price, and shareability must be 1–5")

    normalized = [s * 20 for s in raw_scores]  # 1-5 → 20-100
    trend_norm = trend_score * 20
    ip_norm = ip_score * 20

    all_scores = normalized + [trend_norm, ip_norm]
    weights = [w for _, _, w in DIMENSIONS]
    total = sum(s * w for s, w in zip(all_scores, weights)) / 100
    total_int = round(total)

    if total_int >= 75:
        verdict = "GO"
        advice = (
            "Strong viral signals. Move fast: list via dropship this week, "
            "run a small video ad, and set up Rijoy share-rewards to amplify. "
            "Source on 1688 only after you see consistent orders."
        )
    elif total_int >= 50:
        verdict = "GO WITH CAUTION"
        advice = (
            "Some dimensions are solid but others flag risk. Test with "
            "dropship and a minimal ad budget before committing to inventory. "
            "Watch the trend lifecycle closely — if engagement is already "
            "flattening, the window may be shorter than expected."
        )
    else:
        verdict = "PASS"
        advice = (
            "The numbers don't support jumping in. Either the visual hook "
            "is too weak, the trend is declining, or IP risk is too high. "
            "Look for a different product or wait for the next wave."
        )

    labels = [
        f"Visual Hook:   {visual_hook}/5",
        f"Impulse Price: {impulse_price}/5",
        f"Shareability:  {shareability}/5",
        f"Trend Stage:   {trend_stage} ({trend_score}/5)",
        f"IP Risk:       {ip_risk} ({ip_score}/5)",
    ]

    report = "=" * 44 + "\n"
    report += "  VIRAL POTENTIAL ASSESSMENT\n"
    report += "=" * 44 + "\n\n"
    for (_, label, w), display in zip(DIMENSIONS, labels):
        report += f"  {display:<36} weight {w}%\n"
    report += f"\n  SCORE: {total_int} / 100\n"
    report += f"  VERDICT: {verdict}\n"
    report += "-" * 44 + "\n"
    report += f"  {advice}\n"
    report += "=" * 44 + "\n"

    return total_int, verdict, report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score a product's viral potential and get a go/no-go recommendation."
    )
    parser.add_argument(
        "--visual-hook", type=int, required=True,
        help="Visual impact / 3-second hook power (1–5)",
    )
    parser.add_argument(
        "--impulse-price", type=int, required=True,
        help="How well the price fits impulse-buy range (1–5)",
    )
    parser.add_argument(
        "--shareability", type=int, required=True,
        help="Will buyers film and share? (1–5)",
    )
    parser.add_argument(
        "--trend-stage", type=str, required=True,
        choices=["rising", "peak", "declining"],
        help="Current trend lifecycle stage",
    )
    parser.add_argument(
        "--ip-risk", type=str, required=True,
        choices=["low", "medium", "high"],
        help="Intellectual property risk level",
    )
    args = parser.parse_args()

    try:
        _, _, report = score_viral_potential(
            visual_hook=args.visual_hook,
            impulse_price=args.impulse_price,
            shareability=args.shareability,
            trend_stage=args.trend_stage,
            ip_risk=args.ip_risk,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
