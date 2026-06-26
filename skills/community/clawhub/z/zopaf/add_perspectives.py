"""Add three-map perspective data to existing demo-data.json.

No LLM calls — just math. Computes perceived deal clouds, frontiers,
and re-scored trajectories from each party's imperfect view.

Three perspectives:
  - party_a_view: Sam knows own true scores, estimates Morgan's
  - party_b_view: Morgan knows own true scores, estimates Sam's
  - god_view: existing data (true scores for both)
"""
from __future__ import annotations

import json
from copy import deepcopy
from itertools import product

from case import load_case, NegotiationCase, Issue
from scorer import compute_pareto_frontier, compute_anti_frontier


def make_perceived_case(
    base_case: NegotiationCase,
    viewer: str,
    estimated_scores: dict[str, dict[str, int]],
) -> NegotiationCase:
    """Create a modified case where the OTHER party's scores are replaced with estimates.

    viewer="a" means: keep A's true scores, replace B's with estimates.
    viewer="b" means: keep B's true scores, replace A's with estimates.
    """
    case = deepcopy(base_case)
    for issue in case.issues:
        if issue.name in estimated_scores:
            if viewer == "a":
                # A is viewing: replace B's scores with A's estimate of B
                issue.party_b_scores = estimated_scores[issue.name]
            else:
                # B is viewing: replace A's scores with B's estimate of A
                issue.party_a_scores = estimated_scores[issue.name]
    return case


def compute_deal_cloud(case: NegotiationCase) -> list[dict]:
    """Score every possible deal combination."""
    all_deals = case.all_possible_deals()
    cloud = []
    for deal in all_deals:
        a, b = case.score_deal(deal)
        cloud.append({"party_a_score": a, "party_b_score": b})
    return cloud


def compute_frontier_points(case: NegotiationCase) -> list[dict]:
    """Compute Pareto frontier points."""
    frontier = compute_pareto_frontier(case)
    return [{"party_a_score": a, "party_b_score": b} for _, a, b in frontier]


def compute_anti_frontier_points(case: NegotiationCase) -> list[dict]:
    """Compute anti-Pareto frontier points (lower boundary)."""
    af = compute_anti_frontier(case)
    return [{"party_a_score": a, "party_b_score": b} for _, a, b in af]


def rescore_trajectory(
    round_data: list[dict],
    case: NegotiationCase,
) -> list[dict]:
    """Re-score existing trajectory terms using a (possibly modified) case."""
    rescored = []
    for rd in round_data:
        terms = rd.get("terms")
        if terms:
            a, b = case.score_deal(terms)
            rescored.append({
                "round": rd["round"],
                "speaker": rd["speaker"],
                "party_a_score": a,
                "party_b_score": b,
            })
    return rescored


def main():
    case = load_case("cases/vc_term_sheet.yaml")

    # ----- Sam's estimate of Morgan's priorities -----
    # Sam overestimates how much Morgan cares about valuation,
    # and underestimates how much Morgan cares about board seats.
    a_estimates_b = {
        "Pre-Money Valuation": {"$30M": 40, "$35M": 25, "$40M": 10, "$45M": 0},
        "Board Composition": {
            "2 founder, 2 investor, 1 independent": 25,
            "2 founder, 1 investor, 1 independent": 15,
            "2 founder, 1 investor, 0 independent": 5,
            "3 founder, 1 investor, 1 independent": 0,
        },
        "Liquidation Preference": {
            "1x participating": 25,
            "1x participating, 3x cap": 20,
            "1x non-participating": 10,
            "1x non-participating, converts above 2x": 0,
        },
        "Pro-Rata Rights": {
            "Full pro-rata + super pro-rata": 20,
            "Full pro-rata rights": 15,
            "Pro-rata up to 2x ownership": 5,
            "No pro-rata rights": 0,
        },
        "Founder Vesting": {
            "Full 4-year reset": 20,
            "3-year reset, 1-year cliff": 15,
            "2-year acceleration, remaining vests": 5,
            "No reset, full credit for time served": 0,
        },
    }

    # ----- Morgan's estimate of Sam's priorities -----
    # Morgan thinks Sam cares mostly about valuation, underestimates
    # how much Sam values board control and vesting credit.
    b_estimates_a = {
        "Pre-Money Valuation": {"$30M": 0, "$35M": 10, "$40M": 25, "$45M": 40},
        "Board Composition": {
            "2 founder, 2 investor, 1 independent": 0,
            "2 founder, 1 investor, 1 independent": 15,
            "2 founder, 1 investor, 0 independent": 25,
            "3 founder, 1 investor, 1 independent": 30,
        },
        "Liquidation Preference": {
            "1x participating": 0,
            "1x participating, 3x cap": 10,
            "1x non-participating": 25,
            "1x non-participating, converts above 2x": 35,
        },
        "Pro-Rata Rights": {
            "Full pro-rata + super pro-rata": 0,
            "Full pro-rata rights": 5,
            "Pro-rata up to 2x ownership": 15,
            "No pro-rata rights": 25,
        },
        "Founder Vesting": {
            "Full 4-year reset": 0,
            "3-year reset, 1-year cliff": 10,
            "2-year acceleration, remaining vests": 20,
            "No reset, full credit for time served": 30,
        },
    }

    # Build perceived cases
    case_a_view = make_perceived_case(case, "a", a_estimates_b)
    case_b_view = make_perceived_case(case, "b", b_estimates_a)

    # Compute perceived deal clouds and frontiers
    a_cloud = compute_deal_cloud(case_a_view)
    b_cloud = compute_deal_cloud(case_b_view)
    a_frontier = compute_frontier_points(case_a_view)
    b_frontier = compute_frontier_points(case_b_view)

    # Load existing demo data
    with open("web/public/demo-data.json") as f:
        demo_data = json.load(f)

    # Re-score trajectories from each perspective
    for mode in ["naive", "smart", "both_smart"]:
        rd = demo_data[mode]["round_data"]
        demo_data[mode]["trajectory_a_view"] = rescore_trajectory(rd, case_a_view)
        demo_data[mode]["trajectory_b_view"] = rescore_trajectory(rd, case_b_view)
        # Original trajectory is already the god view

    # Add perspective data
    demo_data["party_a_view"] = {
        "label": f"{demo_data['party_a_name']}'s Map",
        "description": "What Sam thinks the deal space looks like",
        "deal_cloud": a_cloud,
        "frontier": a_frontier,
    }
    demo_data["party_b_view"] = {
        "label": f"{demo_data['party_b_name']}'s Map",
        "description": "What Morgan thinks the deal space looks like",
        "deal_cloud": b_cloud,
        "frontier": b_frontier,
    }

    with open("web/public/demo-data.json", "w") as f:
        json.dump(demo_data, f, indent=2)

    print("Perspective data added to demo-data.json")
    print(f"  A's perceived frontier: {len(a_frontier)} points")
    print(f"  B's perceived frontier: {len(b_frontier)} points")
    print(f"  A's deal cloud: {len(a_cloud)} deals")
    print(f"  B's deal cloud: {len(b_cloud)} deals")


if __name__ == "__main__":
    main()
