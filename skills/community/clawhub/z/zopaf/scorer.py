"""Scoring and Pareto frontier analysis.

Total score = Σ satisfaction_i * weight_i (scaled to 0-100)

Continuous issues: LP variable v in [min, max]
  satisfaction = (v - min)/(max - min) if best=max, else (max - v)/(max - min)
  score contribution = satisfaction * weight

Discrete issues: binary vars x[j]
  score contribution = satisfaction[j] * weight * x[j]
"""
from __future__ import annotations

from typing import Any

import pulp

from case import NegotiationCase
from elicitation import compute_weighted_score


def _build_problem_vars(case: NegotiationCase, prob: pulp.LpProblem):
    """Create LP variables. Returns (x, v, va_expr, vb_expr).
    Score expressions are in [0, 1] (satisfaction * weight)."""
    x = {}
    v = {}

    va_terms = []
    vb_terms = []

    for issue in case.issues:
        if issue.discrete:
            for label in issue.option_labels:
                x[(issue.name, label)] = pulp.LpVariable(
                    f"x_{issue.name}_{label}", cat="Binary"
                )
            prob += (
                pulp.lpSum(x[(issue.name, label)] for label in issue.option_labels) == 1,
                f"one_option_{issue.name}",
            )
            # score = satisfaction[label] * weight * x[label]
            for label in issue.option_labels:
                va_terms.append(issue.satisfaction_a[label] * issue.weight_a * x[(issue.name, label)])
                vb_terms.append(issue.satisfaction_b[label] * issue.weight_b * x[(issue.name, label)])
        else:
            # Continuous: v in [min, max]
            v[issue.name] = pulp.LpVariable(
                f"v_{issue.name}",
                lowBound=issue.range_min,
                upBound=issue.range_max,
                cat="Continuous",
            )
            rng = issue.range_max - issue.range_min
            if rng > 0:
                # satisfaction_a = (v - min)/rng if best=max, else (max - v)/rng
                # score_a = satisfaction_a * weight_a
                if issue.best_for_a == "max":
                    # sat = (v - min)/rng → score = weight/rng * v - weight*min/rng
                    va_terms.append((issue.weight_a / rng) * v[issue.name] - issue.weight_a * issue.range_min / rng)
                else:
                    # sat = (max - v)/rng → score = -weight/rng * v + weight*max/rng
                    va_terms.append(-(issue.weight_a / rng) * v[issue.name] + issue.weight_a * issue.range_max / rng)

                if issue.best_for_b == "max":
                    vb_terms.append((issue.weight_b / rng) * v[issue.name] - issue.weight_b * issue.range_min / rng)
                else:
                    vb_terms.append(-(issue.weight_b / rng) * v[issue.name] + issue.weight_b * issue.range_max / rng)

    va_expr = pulp.lpSum(va_terms)
    vb_expr = pulp.lpSum(vb_terms)

    return x, v, va_expr, vb_expr


def _extract_deal(case: NegotiationCase, x: dict, v: dict) -> dict[str, Any]:
    """Extract deal values from solved LP variables."""
    deal: dict[str, Any] = {}
    for issue in case.issues:
        if issue.discrete:
            for label in issue.option_labels:
                if pulp.value(x[(issue.name, label)]) > 0.5:
                    deal[issue.name] = label
                    break
        else:
            deal[issue.name] = round(pulp.value(v[issue.name]), 2)
    return deal


def _solve_frontier_point(case, min_a_score_frac):
    """max V_b s.t. V_a >= min_a_score_frac (fraction in [0, 1])."""
    prob = pulp.LpProblem("pareto_point", pulp.LpMaximize)
    x, v, va_expr, vb_expr = _build_problem_vars(case, prob)
    prob += vb_expr
    prob += (va_expr >= min_a_score_frac, "min_party_a")
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    if prob.status != pulp.constants.LpStatusOptimal:
        return None
    deal = _extract_deal(case, x, v)
    a, b = case.score_deal(deal)
    return deal, a, b


def _solve_anti_frontier_point(case, target_a_frac, tolerance=0.02):
    """min V_b s.t. target <= V_a <= target + tolerance."""
    prob = pulp.LpProblem("anti_pareto", pulp.LpMinimize)
    x, v, va_expr, vb_expr = _build_problem_vars(case, prob)
    prob += vb_expr
    prob += (va_expr >= target_a_frac, "min_party_a")
    prob += (va_expr <= target_a_frac + tolerance, "max_party_a")
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    if prob.status != pulp.constants.LpStatusOptimal:
        return None
    deal = _extract_deal(case, x, v)
    a, b = case.score_deal(deal)
    return deal, a, b


def _solve_extremes(case):
    """Find min and max A scores."""
    # Max A
    prob = pulp.LpProblem("max_a", pulp.LpMaximize)
    x, v, va_expr, vb_expr = _build_problem_vars(case, prob)
    prob += va_expr
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    if prob.status != pulp.constants.LpStatusOptimal:
        return None, None
    max_deal = _extract_deal(case, x, v)
    max_a = case.score_deal(max_deal)[0]

    # Min A
    prob2 = pulp.LpProblem("min_a", pulp.LpMinimize)
    x2, v2, va2, vb2 = _build_problem_vars(case, prob2)
    prob2 += va2
    prob2.solve(pulp.PULP_CBC_CMD(msg=0))
    if prob2.status != pulp.constants.LpStatusOptimal:
        return None, None
    min_deal = _extract_deal(case, x2, v2)
    min_a = case.score_deal(min_deal)[0]

    return min_a, max_a


def compute_pareto_frontier(case, num_steps=50):
    """Compute upper frontier by sweeping V_a."""
    min_a, max_a = _solve_extremes(case)
    if min_a is None:
        return []

    # Sweep in fractional score space [0, 1]
    # The VA expression is in [0, sum_of_weights_a] ≈ [0, 1]
    # But score_deal scales to 0-100. Sweep in the fraction space.
    # We need to sweep va_expr, which is in [0, ~1].
    # min_a/100 and max_a/100 give the fraction range.
    frac_min = min_a / 100.0
    frac_max = max_a / 100.0

    frontier_map = {}
    step = max(0.001, (frac_max - frac_min) / num_steps)

    target = frac_min
    while target <= frac_max + step / 2:
        result = _solve_frontier_point(case, target)
        if result:
            deal, a, b = result
            if (a, b) not in frontier_map:
                frontier_map[(a, b)] = deal
        target += step

    # Filter dominated
    scored = [(deal, a, b) for (a, b), deal in frontier_map.items()]
    frontier = []
    for deal, a, b in scored:
        dominated = any(
            (a2 >= a and b2 >= b and (a2 > a or b2 > b))
            for _, a2, b2 in scored
        )
        if not dominated:
            frontier.append((deal, a, b))

    frontier.sort(key=lambda x: x[1])
    return frontier


def compute_anti_frontier(case, num_steps=50):
    """Compute lower frontier by sweeping V_a."""
    min_a, max_a = _solve_extremes(case)
    if min_a is None:
        return []

    frac_min = min_a / 100.0
    frac_max = max_a / 100.0

    frontier_map = {}
    step = max(0.001, (frac_max - frac_min) / num_steps)

    target = frac_min
    while target <= frac_max + step / 2:
        result = _solve_anti_frontier_point(case, target, tolerance=step)
        if result:
            deal, a, b = result
            if (a, b) not in frontier_map:
                frontier_map[(a, b)] = deal
        target += step

    # Lower envelope
    a_to_min_b: dict[int, tuple[dict, int, int]] = {}
    for (a, b), deal in frontier_map.items():
        if a not in a_to_min_b or b < a_to_min_b[a][2]:
            a_to_min_b[a] = (deal, a, b)

    anti = list(a_to_min_b.values())
    anti.sort(key=lambda x: x[1])
    return anti


def analyze_outcome(case, deal):
    """Analyze a negotiation outcome against the Pareto frontier."""
    frontier = compute_pareto_frontier(case)

    if deal is None:
        a_score = case.party_a_batna_score
        b_score = case.party_b_batna_score
        deal_exists = False
    else:
        a_score, b_score = case.score_deal(deal)
        deal_exists = True

    joint = a_score + b_score
    max_joint = max(a + b for _, a, b in frontier) if frontier else 0
    batna_joint = case.party_a_batna_score + case.party_b_batna_score

    available = max_joint - batna_joint
    captured = joint - batna_joint
    pct = (captured / available * 100) if available > 0 else 100.0

    min_dist = float("inf")
    nearest = None
    for f_deal, f_a, f_b in frontier:
        dist = ((a_score - f_a) ** 2 + (b_score - f_b) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            nearest = f_deal

    return {
        "party_a_score": a_score,
        "party_b_score": b_score,
        "joint_score": joint,
        "max_joint_score": max_joint,
        "frontier": frontier,
        "distance_to_frontier": min_dist,
        "nearest_frontier_deal": nearest,
        "value_captured_pct": pct,
        "deal_exists": deal_exists,
    }


def print_analysis(case, deal):
    """Print formatted analysis."""
    r = analyze_outcome(case, deal)
    print(f"\n{'='*60}")
    print("  NEGOTIATION ANALYSIS")
    print(f"{'='*60}")
    if r["deal_exists"]:
        print(f"\n  Deal reached!")
        print(f"\n  Agreed terms:")
        for k, v in deal.items():
            print(f"    {k}: {v}")
    else:
        print(f"\n  No deal — BATNA applies")
    print(f"\n  Scores (0-100):")
    print(f"    {case.party_a_name}: {r['party_a_score']}")
    print(f"    {case.party_b_name}: {r['party_b_score']}")
    print(f"    Joint: {r['joint_score']}")
    print(f"    Max possible: {r['max_joint_score']}")
    print(f"    Value captured: {r['value_captured_pct']:.1f}%")


def compute_weighted_pareto_frontier(case, weights, num_steps=50):
    """Compute Pareto frontier using weighted scores."""
    frontier = compute_pareto_frontier(case, num_steps)
    return [
        (deal, compute_weighted_score(case, deal, weights), b)
        for deal, a, b in frontier
    ]
