"""Interactive CLI for preference elicitation and weight learning.

Walks a user through triad comparisons, solves for their weights,
then demonstrates iso-utility offer generation.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from case import load_case, NegotiationCase
from elicitation import (
    generate_triads,
    format_triad_for_display,
    solve_weights,
    compute_weighted_score,
    generate_iso_utility_offers,
    TriadChoice,
)


def run_elicitation(case: NegotiationCase, num_triads: int = 8):
    """Run the interactive preference elicitation."""
    print(f"\n{'='*60}")
    print(f"  PREFERENCE ELICITATION")
    print(f"  Case: {case.title}")
    print(f"{'='*60}")
    print()
    print("  Instead of asking you to rank and weight issues directly")
    print("  (which humans do poorly), we'll show you sets of three")
    print("  deal options. Just pick the one you'd prefer.")
    print()
    print(f"  Issues on the table:")
    for issue in case.issues:
        opts = ", ".join(f'"{o}"' for o in issue.options)
        print(f"    - {issue.name}: {opts}")
    print()
    print(f"  You'll see {num_triads} comparisons. Let's go.\n")

    triads = generate_triads(case, num_triads=num_triads, issues_per_triad=3)
    choices = []

    for i, triad in enumerate(triads, 1):
        print(f"  --- Comparison {i}/{num_triads} ---")
        print(f"  Issues: {', '.join(triad.issues_subset)}\n")
        print(format_triad_for_display(triad))
        print()

        while True:
            answer = input("  Which do you prefer? (A/B/C): ").strip().upper()
            if answer in ("A", "B", "C"):
                chosen_idx = {"A": 0, "B": 1, "C": 2}[answer]
                choices.append(TriadChoice(triad=triad, chosen_index=chosen_idx))
                break
            print("  Please enter A, B, or C.")
        print()

    # Solve for weights
    print(f"\n{'='*60}")
    print(f"  LEARNED PREFERENCES")
    print(f"{'='*60}\n")

    weights = solve_weights(case, choices)

    # Sort by weight descending
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)

    print("  Your revealed preference weights:\n")
    bar_width = 40
    for issue_name, weight in sorted_weights:
        bar = "█" * int(weight * bar_width)
        print(f"    {issue_name:<25s} {weight:5.1%}  {bar}")
    print()

    return weights


def demo_iso_utility(case: NegotiationCase, weights: dict[str, float]):
    """Demonstrate iso-utility offer generation."""
    print(f"\n{'='*60}")
    print(f"  ISO-UTILITY OFFER SETS")
    print(f"{'='*60}\n")
    print("  These are 3 offers that are equally good FOR YOU.")
    print("  Presenting them to your counterpart reveals THEIR priorities")
    print("  based on which one they gravitate toward.\n")

    # Generate offers at a moderate utility level
    target = 0.5
    offers = generate_iso_utility_offers(
        case, weights, target_score=target, tolerance=0.1, max_offers=3,
    )

    if not offers:
        print("  Could not generate iso-utility offers at this target level.")
        print("  Try adjusting the tolerance or target score.")
        return

    for idx, offer in enumerate(offers):
        label = chr(65 + idx)  # A, B, C
        score = compute_weighted_score(case, offer, weights)
        print(f"  Offer {label} (your utility: {score:.2f}):")
        for issue_name, option in offer.items():
            print(f"    {issue_name}: {option}")
        print()

    print("  All three offers score nearly the same for you.")
    print("  But they vary in HOW they distribute value across issues.")
    print("  Your counterpart's choice tells you what THEY value most.\n")


def main():
    parser = argparse.ArgumentParser(description="Zopaf Preference Elicitation")
    parser.add_argument(
        "case_file",
        nargs="?",
        default="cases/job_offer.yaml",
        help="Path to the negotiation case YAML file",
    )
    parser.add_argument(
        "--triads", "-t",
        type=int,
        default=8,
        help="Number of triad comparisons (default: 8)",
    )
    args = parser.parse_args()

    case_path = Path(args.case_file)
    if not case_path.exists():
        print(f"Error: Case file not found: {case_path}")
        sys.exit(1)

    case = load_case(case_path)

    # Run elicitation
    weights = run_elicitation(case, num_triads=args.triads)

    # Demo iso-utility offers
    demo_iso_utility(case, weights)

    print(f"{'='*60}")
    print(f"  WHAT THIS MEANS")
    print(f"{'='*60}\n")
    print("  These learned weights replace unreliable self-reported rankings.")
    print("  In a real negotiation, Zopaf would use these to:")
    print("    1. Generate optimal offers tailored to your TRUE priorities")
    print("    2. Present iso-utility sets to learn your counterpart's weights")
    print("    3. Guide you toward Pareto-optimal deals on the frontier")
    print()


if __name__ == "__main__":
    main()
