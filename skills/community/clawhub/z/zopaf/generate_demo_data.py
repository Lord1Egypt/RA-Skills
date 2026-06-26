"""Generate demo data for the negotiation map visualization.

Runs naive-vs-naive and smart-vs-naive simulations, extracts per-round
proposed deals, scores them, and outputs JSON for the frontend.
"""
from __future__ import annotations

import json
import os
import sys

import anthropic

from case import load_case, NegotiationCase
from agent import NegotiationAgent
from smart_agent import SmartNegotiationAgent
from simulator import extract_deal_terms
from scorer import compute_pareto_frontier, compute_anti_frontier


def extract_round_offers(message: str, case: NegotiationCase) -> dict | None:
    """Extract proposed deal terms from a single negotiation message."""
    client = anthropic.Anthropic()

    issue_descriptions = []
    for issue in case.issues:
        opts = ", ".join(f'"{o}"' for o in issue.options)
        issue_descriptions.append(f"- {issue.name} (options: {opts})")
    issues_block = "\n".join(issue_descriptions)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="You extract proposed deal terms from negotiation messages. Respond ONLY with the terms, nothing else.",
        messages=[{
            "role": "user",
            "content": f"""Extract the proposed/offered deal terms from this negotiation message.
If the message proposes multiple packages, extract the FIRST one only.

ISSUES AND VALID OPTIONS:
{issues_block}

MESSAGE:
{message}

Respond with ONLY the proposed terms, one per line, in this format:
issue_name: chosen_option

Match to the CLOSEST valid option for each issue.
If an issue is not mentioned, use the middle option.""",
        }],
    )

    text = response.content[0].text.strip()
    terms = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')
            for issue in case.issues:
                if issue.name.lower() == key.lower():
                    # Find closest matching option
                    best_match = None
                    for opt in issue.options:
                        if opt.lower() == value.lower():
                            best_match = opt
                            break
                    if best_match is None:
                        # Fuzzy: pick closest by substring
                        for opt in issue.options:
                            if value.lower() in opt.lower() or opt.lower() in value.lower():
                                best_match = opt
                                break
                    if best_match is None:
                        # Numeric proximity: extract numbers and find closest
                        import re
                        val_nums = re.findall(r'[\d.]+', value)
                        if val_nums:
                            val_num = float(val_nums[0])
                            best_dist = float('inf')
                            for opt in issue.options:
                                opt_nums = re.findall(r'[\d.]+', opt)
                                if opt_nums:
                                    dist = abs(float(opt_nums[0]) - val_num)
                                    if dist < best_dist:
                                        best_dist = dist
                                        best_match = opt
                    if best_match is None:
                        best_match = issue.options[len(issue.options) // 2]
                    terms[issue.name] = best_match
                    break

    # Fill missing issues with middle option
    for issue in case.issues:
        if issue.name not in terms:
            terms[issue.name] = issue.options[len(issue.options) // 2]

    return terms


def run_simulation(case, agent_a, agent_b, label, verbose=True):
    """Run a simulation and collect per-round data."""
    transcript = []
    round_data = []
    b_response = None

    for round_num in range(1, case.max_rounds + 1):
        if verbose:
            print(f"\n  [{label}] Round {round_num}...")

        # Agent A
        if round_num == 1:
            a_response = agent_a.respond()
        else:
            a_response = agent_a.respond(b_response)

        transcript.append((case.party_a_name, a_response))

        # Extract A's proposed terms and score them
        a_terms = extract_round_offers(a_response, case)
        if a_terms:
            a_score_a, a_score_b = case.score_deal(a_terms)
            round_data.append({
                "round": round_num,
                "speaker": case.party_a_name,
                "party_a_score": a_score_a,
                "party_b_score": a_score_b,
                "terms": a_terms,
            })

        if "DEAL AGREED" in a_response.upper():
            break

        # Agent B
        b_response = agent_b.respond(a_response)
        transcript.append((case.party_b_name, b_response))

        b_terms = extract_round_offers(b_response, case)
        if b_terms:
            b_score_a, b_score_b = case.score_deal(b_terms)
            round_data.append({
                "round": round_num,
                "speaker": case.party_b_name,
                "party_a_score": b_score_a,
                "party_b_score": b_score_b,
                "terms": b_terms,
            })

        if "DEAL AGREED" in b_response.upper():
            break

    # Extract final deal
    full_transcript = "\n\n".join(f"[{name}]: {msg}" for name, msg in transcript)
    deal = extract_deal_terms(full_transcript, case)
    final_scores = None
    if deal:
        a, b = case.score_deal(deal)
        final_scores = {"party_a_score": a, "party_b_score": b}

    # Build simplified transcript for display
    simple_transcript = []
    for name, msg in transcript:
        # Truncate long messages for display
        lines = msg.strip().split("\n")
        summary = "\n".join(lines[:15])
        if len(lines) > 15:
            summary += "\n..."
        simple_transcript.append({"speaker": name, "message": summary})

    return {
        "round_data": round_data,
        "final_deal": deal,
        "final_scores": final_scores,
        "transcript": simple_transcript,
    }


def main():
    case_path = sys.argv[1] if len(sys.argv) > 1 else "cases/vc_term_sheet.yaml"
    case = load_case(case_path)

    print(f"Generating demo data for: {case.title}")

    # Compute Pareto frontier (upper)
    print("\nComputing Pareto frontier...")
    frontier = compute_pareto_frontier(case)
    frontier_points = [{"party_a_score": a, "party_b_score": b, "terms": deal} for deal, a, b in frontier]

    # Compute anti-Pareto frontier (lower)
    print("Computing lower frontier...")
    anti_frontier = compute_anti_frontier(case)
    anti_frontier_points = [{"party_a_score": a, "party_b_score": b} for _, a, b in anti_frontier]

    # Compute all possible deals for the "football" shape
    print("Computing deal space...")
    all_deals = case.all_possible_deals()
    deal_cloud = []
    for deal in all_deals:
        a, b = case.score_deal(deal)
        deal_cloud.append({"party_a_score": a, "party_b_score": b})

    # Run naive vs naive
    print("\nRunning naive vs naive simulation...")
    naive_a = NegotiationAgent(case, "a")
    naive_b = NegotiationAgent(case, "b")
    naive_result = run_simulation(case, naive_a, naive_b, "NAIVE")

    # Run smart vs naive
    print("\nRunning smart vs naive simulation...")
    smart_a = SmartNegotiationAgent(case, "a")
    naive_b2 = NegotiationAgent(case, "b")
    smart_result = run_simulation(case, smart_a, naive_b2, "SMART")

    # Run smart vs smart (both use Zopaf — neutral mediator scenario)
    print("\nRunning smart vs smart simulation...")
    smart_a2 = SmartNegotiationAgent(case, "a")
    smart_b2 = SmartNegotiationAgent(case, "b")
    both_result = run_simulation(case, smart_a2, smart_b2, "BOTH SMART")

    # Assemble output
    demo_data = {
        "case_title": case.title,
        "party_a_name": case.party_a_name,
        "party_b_name": case.party_b_name,
        "frontier": frontier_points,
        "anti_frontier": anti_frontier_points,
        "deal_cloud": deal_cloud,
        "naive": naive_result,
        "smart": smart_result,
        "both_smart": both_result,
    }

    # Add three-map perspective data
    print("\nComputing perspective data for three maps...")
    from add_perspectives import (
        make_perceived_case,
        compute_deal_cloud,
        compute_frontier_points,
        compute_anti_frontier_points,
        rescore_trajectory,
    )
    from add_perspectives import main as _get_estimates

    # Import the hardcoded estimates
    # What Founder thinks VC values (slightly off from reality)
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
    # What VC thinks Founder values (slightly off from reality)
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

    case_a_view = make_perceived_case(case, "a", a_estimates_b)
    case_b_view = make_perceived_case(case, "b", b_estimates_a)

    demo_data["party_a_view"] = {
        "label": f"{case.party_a_name}'s Map",
        "description": f"What {case.party_a_name.split(' ')[0]} thinks the deal space looks like",
        "deal_cloud": compute_deal_cloud(case_a_view),
        "frontier": compute_frontier_points(case_a_view),
        "anti_frontier": compute_anti_frontier_points(case_a_view),
    }
    demo_data["party_b_view"] = {
        "label": f"{case.party_b_name}'s Map",
        "description": f"What {case.party_b_name.split(' ')[0]} thinks the deal space looks like",
        "deal_cloud": compute_deal_cloud(case_b_view),
        "frontier": compute_frontier_points(case_b_view),
        "anti_frontier": compute_anti_frontier_points(case_b_view),
    }

    for mode in ["naive", "smart", "both_smart"]:
        rd = demo_data[mode]["round_data"]
        demo_data[mode]["trajectory_a_view"] = rescore_trajectory(rd, case_a_view)
        demo_data[mode]["trajectory_b_view"] = rescore_trajectory(rd, case_b_view)

    output_path = "web/public/demo-data.json"
    with open(output_path, "w") as f:
        json.dump(demo_data, f, indent=2)

    print(f"\nDemo data written to {output_path}")
    print(f"  Frontier points: {len(frontier_points)}")
    print(f"  Deal cloud: {len(deal_cloud)}")
    print(f"  Naive rounds: {len(naive_result['round_data'])}")
    print(f"  Smart rounds: {len(smart_result['round_data'])}")


if __name__ == "__main__":
    main()
