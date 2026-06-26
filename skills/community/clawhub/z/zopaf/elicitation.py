"""Preference elicitation via triad comparisons and weight solving.

Instead of asking users to rank/weight issues directly (which humans do poorly),
we show triads of option bundles and ask "which matters most?" Repeated choices
reveal a utility function through conjoint-style analysis.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Tuple, Dict, Optional

import numpy as np

from case import NegotiationCase, Issue


@dataclass
class Triad:
    """Three option bundles shown to the user for comparison."""
    issues_subset: list[str]          # which issues are varied
    bundles: list[dict[str, str]]     # 3 bundles, each maps issue_name -> option
    bundle_labels: list[str]          # human-readable labels A/B/C


@dataclass
class TriadChoice:
    """A user's choice from a triad."""
    triad: Triad
    chosen_index: int  # 0, 1, or 2


def generate_triad(case: NegotiationCase, num_issues: int = 3) -> Triad:
    """Generate a triad of option bundles across a random subset of issues.

    Each bundle assigns a random option to each issue in the subset.
    We ensure all three bundles are distinct.
    """
    # Pick a random subset of issues
    issues = case.issues
    k = min(num_issues, len(issues))
    subset = random.sample(issues, k)
    subset_names = [issue.name for issue in subset]

    # Generate 3 distinct bundles
    bundles = []
    seen = set()
    max_attempts = 100

    while len(bundles) < 3 and max_attempts > 0:
        bundle = {}
        for issue in subset:
            bundle[issue.name] = random.choice(issue.options)
        key = tuple(sorted(bundle.items()))
        if key not in seen:
            seen.add(key)
            bundles.append(bundle)
        max_attempts -= 1

    # If we couldn't generate 3 distinct bundles (very small option space),
    # use systematic variation
    if len(bundles) < 3:
        bundles = _systematic_triads(subset)

    labels = ["A", "B", "C"]
    return Triad(
        issues_subset=subset_names,
        bundles=bundles[:3],
        bundle_labels=labels,
    )


def _systematic_triads(issues: list[Issue]) -> list[dict[str, str]]:
    """Generate 3 systematically varied bundles when random fails."""
    bundles = []
    for offset in range(3):
        bundle = {}
        for issue in issues:
            idx = offset % len(issue.options)
            bundle[issue.name] = issue.options[idx]
        bundles.append(bundle)
    return bundles


def generate_triads(
    case: NegotiationCase,
    num_triads: int = 10,
    issues_per_triad: int = 3,
) -> list[Triad]:
    """Generate a set of triads for preference elicitation.

    Aims for good coverage of all issues and option combinations.
    """
    triads = []
    for _ in range(num_triads):
        triad = generate_triad(case, issues_per_triad)
        triads.append(triad)
    return triads


def format_triad_for_display(triad: Triad) -> str:
    """Format a triad for terminal display."""
    lines = []
    header = "  " + "".join(f"{'Option ' + label:>25s}" for label in triad.bundle_labels)
    lines.append(header)
    lines.append("  " + "-" * 75)

    for issue_name in triad.issues_subset:
        row = f"  {issue_name:<20s}"
        for bundle in triad.bundles:
            row += f"{bundle[issue_name]:>25s}"
        lines.append(row)

    return "\n".join(lines)


def solve_weights(
    case: NegotiationCase,
    choices: list[TriadChoice],
) -> dict[str, float]:
    """Solve for issue weights from triad choices using least-squares.

    Model: Each issue has a weight w_i. Each option within an issue has
    a "desirability" score d_{i,j}. The user chooses the bundle with the
    highest weighted desirability sum.

    We use a simplified approach:
    - Option desirability within each issue is encoded as position
      (first option = 0, last option = 1, linearly spaced)
    - We solve for weights that best explain the observed choices
      using a margin-based loss: chosen bundle should score higher
      than unchosen bundles.
    """
    issues = case.issues
    issue_names = [issue.name for issue in issues]
    n_issues = len(issues)

    # Build option desirability maps (linear scale 0 to 1)
    option_scores = {}
    for issue in issues:
        n_opts = len(issue.options)
        for idx, opt in enumerate(issue.options):
            if n_opts == 1:
                option_scores[(issue.name, opt)] = 1.0
            else:
                option_scores[(issue.name, opt)] = idx / (n_opts - 1)

    if not choices:
        # No data — return uniform weights
        return {name: 1.0 / n_issues for name in issue_names}

    # Build the constraint system
    # For each choice: chosen_bundle should score > each unchosen bundle
    # This gives us 2 constraints per choice (chosen > unchosen_1, chosen > unchosen_2)
    A_rows = []
    for choice in choices:
        triad = choice.triad
        chosen_bundle = triad.bundles[choice.chosen_index]
        unchosen_indices = [i for i in range(3) if i != choice.chosen_index]

        for unchosen_idx in unchosen_indices:
            unchosen_bundle = triad.bundles[unchosen_idx]
            # For each issue in the subset, compute the desirability difference
            row = np.zeros(n_issues)
            for i, issue_name in enumerate(issue_names):
                if issue_name in chosen_bundle and issue_name in unchosen_bundle:
                    chosen_d = option_scores.get((issue_name, chosen_bundle[issue_name]), 0.5)
                    unchosen_d = option_scores.get((issue_name, unchosen_bundle[issue_name]), 0.5)
                    row[i] = chosen_d - unchosen_d
            A_rows.append(row)

    A = np.array(A_rows)
    # We want A @ w > 0 for all rows (chosen scores higher)
    # Solve via least squares with target margin of 1.0
    b = np.ones(len(A_rows))

    # Solve with non-negative least squares to get positive weights
    from scipy.optimize import nnls
    weights, _ = nnls(A, b)

    # Normalize to sum to 1
    total = weights.sum()
    if total > 0:
        weights = weights / total
    else:
        weights = np.ones(n_issues) / n_issues

    return {issue_names[i]: float(weights[i]) for i in range(n_issues)}


def compute_weighted_score(
    case: NegotiationCase,
    deal: dict[str, str],
    weights: dict[str, float],
) -> float:
    """Score a deal using learned weights instead of fixed point values.

    For each issue, the score is: weight * option_position (0 to 1 scale).
    Higher option positions = more desirable to this party.
    """
    score = 0.0
    for issue in case.issues:
        option = deal.get(issue.name)
        if option is not None:
            idx = issue.options.index(option) if option in issue.options else 0
            n_opts = len(issue.options)
            desirability = idx / (n_opts - 1) if n_opts > 1 else 1.0
            weight = weights.get(issue.name, 0.0)
            score += weight * desirability
    return score


def generate_iso_utility_offers(
    case: NegotiationCase,
    weights: dict[str, float],
    target_score: float,
    tolerance: float = 0.05,
    max_offers: int = 3,
) -> list[dict[str, str]]:
    """Generate offers that have approximately the same utility for one party.

    These iso-utility offers can be presented to the counterpart.
    Whichever they prefer reveals information about THEIR weights.

    Args:
        case: The negotiation case
        weights: The presenting party's learned weights
        target_score: Target weighted score (0 to 1)
        tolerance: How close to target_score a deal must be
        max_offers: Number of offers to return
    """
    all_deals = case.all_possible_deals()

    # Score each deal and find ones near the target
    scored_deals = []
    for deal in all_deals:
        score = compute_weighted_score(case, deal, weights)
        if abs(score - target_score) <= tolerance:
            scored_deals.append((deal, score))

    # Sort by closeness to target
    scored_deals.sort(key=lambda x: abs(x[1] - target_score))

    # Select diverse offers (maximize variation across issues)
    if len(scored_deals) <= max_offers:
        return [d for d, _ in scored_deals]

    selected = [scored_deals[0]]
    for deal, score in scored_deals[1:]:
        if len(selected) >= max_offers:
            break
        # Check if this deal differs enough from already selected
        differs = False
        for sel_deal, _ in selected:
            diff_count = sum(
                1 for k in deal if deal[k] != sel_deal[k]
            )
            if diff_count >= 2:
                differs = True
                break
        if differs:
            selected.append((deal, score))

    # If we didn't get enough diverse ones, fill with closest
    if len(selected) < max_offers:
        for deal, score in scored_deals:
            if len(selected) >= max_offers:
                break
            if (deal, score) not in selected:
                selected.append((deal, score))

    return [d for d, _ in selected[:max_offers]]
