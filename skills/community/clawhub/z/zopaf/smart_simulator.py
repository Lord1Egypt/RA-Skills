"""Simulation runner that pits a SmartAgent against a naive agent,
or runs both as smart agents, then compares outcomes.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from case import load_case, NegotiationCase
from agent import NegotiationAgent
from smart_agent import SmartNegotiationAgent, _build_weight_map
from simulator import extract_deal_terms
from scorer import print_analysis, print_weighted_analysis


def run_smart_vs_naive(case: NegotiationCase, smart_party: str = "a") -> dict:
    """Run a negotiation: SmartAgent vs naive NegotiationAgent.

    Args:
        case: The negotiation case
        smart_party: Which party uses the smart strategy ("a" or "b")
    """
    if smart_party == "a":
        agent_a = SmartNegotiationAgent(case, "a")
        agent_b = NegotiationAgent(case, "b")
        smart_name = case.party_a_name
        naive_name = case.party_b_name
    else:
        agent_a = NegotiationAgent(case, "a")
        agent_b = SmartNegotiationAgent(case, "b")
        smart_name = case.party_b_name
        naive_name = case.party_a_name

    print(f"\n  Strategy: {smart_name} uses Zopaf framework")
    print(f"           {naive_name} negotiates naively\n")

    transcript = []
    b_response = None

    for round_num in range(1, case.max_rounds + 1):
        print(f"\n{'='*60}")
        print(f"  ROUND {round_num}")
        print(f"{'='*60}")

        # Agent A's turn
        if round_num == 1:
            a_response = agent_a.respond()
        else:
            a_response = agent_a.respond(b_response)

        transcript.append((case.party_a_name, a_response))
        print(f"\n[{case.party_a_name}]:")
        print(a_response)

        if "DEAL AGREED" in a_response.upper():
            break

        # Agent B's turn
        b_response = agent_b.respond(a_response)
        transcript.append((case.party_b_name, b_response))
        print(f"\n[{case.party_b_name}]:")
        print(b_response)

        if "DEAL AGREED" in b_response.upper():
            break

    # Extract deal
    full_transcript = "\n\n".join(f"[{name}]: {msg}" for name, msg in transcript)
    deal = extract_deal_terms(full_transcript, case)
    rounds = min((len(transcript) + 1) // 2, case.max_rounds)

    # Get smart agent's inferred weights
    if smart_party == "a":
        inferred = agent_a.inferred_opponent_weights
    else:
        inferred = agent_b.inferred_opponent_weights

    return {
        "transcript": transcript,
        "deal": deal,
        "rounds": rounds,
        "inferred_opponent_weights": inferred,
    }


def run_comparison(case: NegotiationCase) -> None:
    """Run two simulations — naive vs naive, then smart vs naive — and compare."""
    from simulator import run_negotiation
    from scorer import analyze_outcome

    print(f"\n{'#'*60}")
    print(f"  ZOPAF A/B TEST")
    print(f"  Case: {case.title}")
    print(f"{'#'*60}")

    # Run 1: Naive vs Naive
    print(f"\n{'#'*60}")
    print(f"  RUN 1: NAIVE vs NAIVE")
    print(f"{'#'*60}")
    naive_result = run_negotiation(case, verbose=True)
    naive_analysis = analyze_outcome(case, naive_result["deal"])

    # Run 2: Smart vs Naive
    print(f"\n{'#'*60}")
    print(f"  RUN 2: SMART (Zopaf) vs NAIVE")
    print(f"{'#'*60}")
    smart_result = run_smart_vs_naive(case, smart_party="a")
    smart_analysis = analyze_outcome(case, smart_result["deal"])

    # Comparison
    print(f"\n{'#'*60}")
    print(f"  HEAD-TO-HEAD COMPARISON")
    print(f"{'#'*60}")

    print(f"\n  {'':30s} {'Naive vs Naive':>18s}  {'Smart vs Naive':>18s}")
    print(f"  {'-'*68}")

    if naive_result["deal"]:
        na, nb = naive_analysis["party_a_score"], naive_analysis["party_b_score"]
        print(f"  {case.party_a_name + ' score':<30s} {na:>18d}  {smart_analysis['party_a_score']:>18d}")
        print(f"  {case.party_b_name + ' score':<30s} {nb:>18d}  {smart_analysis['party_b_score']:>18d}")
    else:
        print(f"  {'(no deal)':>30s}")

    nj = naive_analysis["joint_score"]
    sj = smart_analysis["joint_score"]
    print(f"  {'Joint value':<30s} {nj:>18d}  {sj:>18d}")
    print(f"  {'Value captured':<30s} {naive_analysis['value_captured_pct']:>17.1f}%  {smart_analysis['value_captured_pct']:>17.1f}%")
    print(f"  {'Distance to frontier':<30s} {naive_analysis['distance_to_frontier']:>17.1f}   {smart_analysis['distance_to_frontier']:>17.1f} ")
    print(f"  {'Rounds':<30s} {naive_result['rounds']:>18d}  {smart_result['rounds']:>18d}")

    diff = sj - nj
    if diff > 0:
        print(f"\n  Zopaf framework created {diff} additional points of joint value!")
    elif diff < 0:
        print(f"\n  Naive agents found {-diff} more joint value this time.")
        print(f"  (Run again — LLM negotiations are stochastic.)")
    else:
        print(f"\n  Same joint value — but check the distribution and frontier distance.")

    if smart_result.get("inferred_opponent_weights"):
        print(f"\n  Smart agent's inferred opponent weights:")
        for name, w in sorted(
            smart_result["inferred_opponent_weights"].items(),
            key=lambda x: -x[1],
        ):
            bar = "█" * int(w * 30)
            print(f"    {name:<25s} {w:5.1%}  {bar}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Zopaf Smart Negotiation Simulator")
    parser.add_argument(
        "case_file",
        nargs="?",
        default="cases/kdh_walmart.yaml",
        help="Path to the negotiation case YAML file",
    )
    parser.add_argument(
        "--mode",
        choices=["smart", "compare"],
        default="smart",
        help="'smart' = Smart vs Naive, 'compare' = run both and compare",
    )
    parser.add_argument(
        "--smart-party",
        choices=["a", "b"],
        default="a",
        help="Which party uses the Zopaf smart strategy (default: a)",
    )
    args = parser.parse_args()

    case_path = Path(args.case_file)
    if not case_path.exists():
        print(f"Error: Case file not found: {case_path}")
        sys.exit(1)

    case = load_case(case_path)

    if args.mode == "compare":
        run_comparison(case)
    else:
        print(f"\n{'#'*60}")
        print(f"  ZOPAF SMART NEGOTIATION")
        print(f"  Case: {case.title}")
        print(f"  {case.party_a_name} vs {case.party_b_name}")
        print(f"{'#'*60}")

        result = run_smart_vs_naive(case, smart_party=args.smart_party)
        print_analysis(case, result["deal"])

        if result.get("inferred_opponent_weights"):
            print(f"  Smart agent's inferred opponent weights:")
            for name, w in sorted(
                result["inferred_opponent_weights"].items(),
                key=lambda x: -x[1],
            ):
                bar = "█" * int(w * 30)
                print(f"    {name:<25s} {w:5.1%}  {bar}")
            print()


if __name__ == "__main__":
    main()
