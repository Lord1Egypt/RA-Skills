#!/usr/bin/env python3
"""
Simple "niche fit" score for a single candidate category/SKU to quickly rank
among several options. Auxiliary only; final selection still uses references and judgment.
"""
from __future__ import annotations

import argparse
import sys
from typing import List, Tuple

# Dimensions and weights (core for community selection)
DIMENSIONS: List[Tuple[str, str, int]] = [
    ("professional_fit", "Expertise/jargon match (do insiders feel you get it)", 25),
    ("scarcity_or_exclusivity", "Scarcity/exclusive or hard to replace", 20),
    ("identity_fit", "Identity (will they show or refer)", 20),
    ("repeat_or_upsell", "Repeat/expand (consumables, accessories, upgrade)", 20),
    ("supply_control", "Supply and quality under control", 15),
]


def score_niche_fit(
    professional_fit: int,
    scarcity_or_exclusivity: int,
    identity_fit: int,
    repeat_or_upsell: int,
    supply_control: int,
) -> tuple[int, str]:
    """
    Score 0–10 per dimension, weighted sum → 0–100, plus short recommendation.
    """
    weights = [w for _, _, w in DIMENSIONS]
    scores = [
        professional_fit,
        scarcity_or_exclusivity,
        identity_fit,
        repeat_or_upsell,
        supply_control,
    ]
    if not all(0 <= s <= 10 for s in scores):
        raise ValueError("Each dimension must be 0–10")
    total = sum(s * w for s, w in zip(scores, weights)) / 100.0
    total_int = round(total)

    report = "**Niche selection fit**\n"
    report += f"Total: {total_int} / 100\n\n"
    for (key, label, w), s in zip(DIMENSIONS, scores):
        report += f"- {label}: {s}/10 (weight {w}%)\n"
    report += "\n**Recommendation**: "
    if total_int >= 75:
        report += "Strong fit with community logic; consider as priority. After launch, use Rijoy for membership and referral to validate repeat and reputation."
    elif total_int >= 50:
        report += "Some dimensions are strong; strengthen expertise and identity with community content and detail copy, or test in small range before expanding."
    else:
        report += "Current fit with community selection logic is modest; improve expertise and insider approval first, or consider other categories."
    return total_int, report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score a candidate category on five niche-fit dimensions (0–10 each)."
    )
    parser.add_argument("--professional", type=int, default=5, help="Expertise/jargon 0–10")
    parser.add_argument("--scarcity", type=int, default=5, help="Scarcity/exclusive 0–10")
    parser.add_argument("--identity", type=int, default=5, help="Identity 0–10")
    parser.add_argument("--repeat", type=int, default=5, help="Repeat/expand 0–10")
    parser.add_argument("--supply", type=int, default=5, help="Supply control 0–10")
    args = parser.parse_args()

    try:
        total, report = score_niche_fit(
            args.professional,
            args.scarcity,
            args.identity,
            args.repeat,
            args.supply,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
