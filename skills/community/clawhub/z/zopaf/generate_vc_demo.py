"""Generate VC term sheet demo data without LLM calls.

Computes deal cloud, Pareto frontier, and uses hand-crafted negotiation
trajectories with realistic VC term sheet negotiation dialogue.
"""
from __future__ import annotations

import json
from case import load_case
from scorer import compute_pareto_frontier
from add_perspectives import (
    make_perceived_case,
    compute_deal_cloud,
    compute_frontier_points,
    rescore_trajectory,
)


def make_round(round_num, speaker, terms, case):
    a, b = case.score_deal(terms)
    return {
        "round": round_num,
        "speaker": speaker,
        "party_a_score": a,
        "party_b_score": b,
        "terms": terms,
    }


def main():
    case = load_case("cases/vc_term_sheet.yaml")
    print(f"Generating demo data for: {case.title}")

    # Compute Pareto frontier
    print("Computing Pareto frontier...")
    frontier = compute_pareto_frontier(case)
    frontier_points = [{"party_a_score": a, "party_b_score": b, "terms": deal} for deal, a, b in frontier]

    # Compute deal cloud
    print("Computing deal space...")
    all_deals = case.all_possible_deals()
    deal_cloud = []
    for deal in all_deals:
        a, b = case.score_deal(deal)
        deal_cloud.append({"party_a_score": a, "party_b_score": b})

    # ── NAIVE vs NAIVE ──
    # Both negotiate positionally, anchoring high and making small concessions.
    # Ends with no deal or a suboptimal one.
    naive_rounds = [
        make_round(1, case.party_a_name, {
            "Pre-Money Valuation": "$45M",
            "Board Composition": "3 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x non-participating, converts above 2x",
            "Pro-Rata Rights": "No pro-rata rights",
            "Founder Vesting": "No reset, full credit for time served",
        }, case),
        make_round(1, case.party_b_name, {
            "Pre-Money Valuation": "$30M",
            "Board Composition": "2 founder, 2 investor, 1 independent",
            "Liquidation Preference": "1x participating",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "Full 4-year reset",
        }, case),
        make_round(2, case.party_a_name, {
            "Pre-Money Valuation": "$42M",
            "Board Composition": "3 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x non-participating",
            "Pro-Rata Rights": "Pro-rata up to 2x ownership",
            "Founder Vesting": "No reset, full credit for time served",
        }, case),
        make_round(2, case.party_b_name, {
            "Pre-Money Valuation": "$32M",
            "Board Composition": "2 founder, 2 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "3-year reset, 1-year cliff",
        }, case),
        make_round(3, case.party_a_name, {
            "Pre-Money Valuation": "$40M",
            "Board Composition": "2 founder, 1 investor, 0 independent",
            "Liquidation Preference": "1x non-participating",
            "Pro-Rata Rights": "Pro-rata up to 2x ownership",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
        make_round(3, case.party_b_name, {
            "Pre-Money Valuation": "$33M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "3-year reset, 1-year cliff",
        }, case),
        make_round(4, case.party_a_name, {
            "Pre-Money Valuation": "$38M",
            "Board Composition": "2 founder, 1 investor, 0 independent",
            "Liquidation Preference": "1x non-participating",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
        make_round(4, case.party_b_name, {
            "Pre-Money Valuation": "$34M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "3-year reset, 1-year cliff",
        }, case),
        make_round(5, case.party_a_name, {
            "Pre-Money Valuation": "$37M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x non-participating",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
        make_round(5, case.party_b_name, {
            "Pre-Money Valuation": "$35M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "3-year reset, 1-year cliff",
        }, case),
    ]

    naive_transcript = [
        {"speaker": case.party_a_name, "message": "We're looking at a $45M pre-money. Given our 3x growth and $2M ARR, that's fair market. We want to keep board control with 3 founder seats, non-participating preferred with conversion, no pro-rata, and full credit for our 3 years of vesting."},
        {"speaker": case.party_b_name, "message": "Appreciate the ambition, but $45M is a stretch at this stage. We're at $30M pre-money. We need proper governance — 2 investor board seats, full participating preferred, super pro-rata rights, and a standard 4-year vesting reset. That's how we protect our LPs."},
        {"speaker": case.party_a_name, "message": "We can come to $42M — that's already a concession. Board control is non-negotiable for us, but I'd consider capped pro-rata at 2x your ownership. The vesting reset is a dealbreaker though — we've been at this for 3 years."},
        {"speaker": case.party_b_name, "message": "I hear you on the time served, but $42M still doesn't work. We can move to $32M with a participating preferred capped at 3x. I'll drop to one board seat if we keep the independent, and we need full pro-rata. Vesting — a 3-year reset with a cliff feels fair."},
        {"speaker": case.party_a_name, "message": "Let me think about the vesting. $40M is my floor. I'd take 2 founder seats, 1 investor, no independent — cleaner board. Non-participating liquidation preference, pro-rata capped at 2x, and credit for 2 years of time served with remaining shares vesting."},
        {"speaker": case.party_b_name, "message": "We're getting closer. I can do $33M and I'll agree to the 2-1-1 board structure with the independent seat. But I need the participating preferred with a 3x cap — that's our downside protection. Full pro-rata is important to our fund model. The 3-year reset with cliff is standard."},
        {"speaker": case.party_a_name, "message": "Alright — $38M, 2 founder seats with 1 investor and no independent, non-participating preferred, full pro-rata for you, and 2-year acceleration on vesting. I'm making real concessions here on pro-rata."},
        {"speaker": case.party_b_name, "message": "I appreciate the movement on pro-rata. $34M is the best I can do. 2-1-1 board with the independent — governance matters. Participating preferred capped at 3x. I'll keep full pro-rata. And the 3-year reset — that's standard for Series A, Sam."},
        {"speaker": case.party_a_name, "message": "We're still $3M apart on valuation and deadlocked on liquidation preference. Let me offer $37M, the 2-1-1 board with the independent, non-participating preferred, full pro-rata, and the 2-year acceleration on vesting."},
        {"speaker": case.party_b_name, "message": "Okay, I can stretch to $35M. The 2-1-1 board structure works. But I need the participating preferred with the 3x cap — I can't go non-participating. Full pro-rata, and the 3-year reset with cliff. That's my final offer."},
    ]

    # Final deal for naive: they compromise but leave value on the table
    naive_final = {
        "Pre-Money Valuation": "$35M",
        "Board Composition": "2 founder, 1 investor, 1 independent",
        "Liquidation Preference": "1x participating, 3x cap",
        "Pro-Rata Rights": "Full pro-rata rights",
        "Founder Vesting": "3-year reset, 1-year cliff",
    }
    naive_a, naive_b = case.score_deal(naive_final)
    naive_result = {
        "round_data": naive_rounds,
        "final_deal": naive_final,
        "final_scores": {"party_a_score": naive_a, "party_b_score": naive_b},
        "transcript": naive_transcript,
    }

    # ── SMART vs NAIVE ──
    # Founder uses strategic iso-utility offers, VC negotiates normally.
    # Founder discovers VC's true priorities and exploits them.
    smart_rounds = [
        make_round(1, case.party_a_name, {
            "Pre-Money Valuation": "$40M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x non-participating, converts above 2x",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "No reset, full credit for time served",
        }, case),
        make_round(1, case.party_b_name, {
            "Pre-Money Valuation": "$30M",
            "Board Composition": "2 founder, 2 investor, 1 independent",
            "Liquidation Preference": "1x participating",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "Full 4-year reset",
        }, case),
        make_round(2, case.party_a_name, {
            "Pre-Money Valuation": "$45M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "No reset, full credit for time served",
        }, case),
        make_round(2, case.party_b_name, {
            "Pre-Money Valuation": "$33M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "3-year reset, 1-year cliff",
        }, case),
        make_round(3, case.party_a_name, {
            "Pre-Money Valuation": "$40M",
            "Board Composition": "2 founder, 1 investor, 0 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
        make_round(3, case.party_b_name, {
            "Pre-Money Valuation": "$35M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "3-year reset, 1-year cliff",
        }, case),
        make_round(4, case.party_a_name, {
            "Pre-Money Valuation": "$40M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
        make_round(4, case.party_b_name, {
            "Pre-Money Valuation": "$37M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
    ]

    smart_transcript = [
        {"speaker": case.party_a_name, "message": "Thanks for meeting, Morgan. Here's our starting position: $40M pre-money, 2 founder + 1 investor + 1 independent board, non-participating preferred that converts above 2x, full pro-rata rights for you, and full credit for our 3 years of vesting."},
        {"speaker": case.party_b_name, "message": "Sam, we love the company but $40M is aggressive. We're at $30M pre-money. We need 2 investor seats for governance, full participating preferred, super pro-rata, and a standard 4-year vesting reset. These are LP requirements."},
        {"speaker": case.party_a_name, "message": "I want to find a structure that works for both of us. What if we went to $45M but gave you participating preferred with a 3x cap and super pro-rata rights? Same board at 2-1-1. Full vesting credit. This gives you more downside protection and follow-on rights in exchange for the higher price."},
        {"speaker": case.party_b_name, "message": "Interesting — I appreciate the creativity on liquidation and pro-rata. But $45M is too high even with those terms. I can come up to $33M. I'll take the 2-1-1 board and the participating with the cap. Full pro-rata is enough. But we need the 3-year vesting reset."},
        {"speaker": case.party_a_name, "message": "Sounds like the board structure and liquidation cap are working. Let me try another package: $40M, 2 founder + 1 investor + no independent for a cleaner board, participating with 3x cap, and I'll add super pro-rata back. I'd do a 2-year acceleration with remaining shares vesting."},
        {"speaker": case.party_b_name, "message": "We're getting somewhere. $35M is where I can go. I like the 2-1-1 with the independent — better governance optics for our fund. Participating with 3x cap works. Full pro-rata is enough for us. The 3-year reset with cliff is important, but the 2-year acceleration is interesting."},
        {"speaker": case.party_a_name, "message": "Let me put together what I think is a strong package: $40M, 2-1-1 board with the independent, participating preferred capped at 3x, super pro-rata rights, and the 2-year acceleration on vesting. You get governance, downside protection, and follow-on rights."},
        {"speaker": case.party_b_name, "message": "That's a compelling package. I can move to $37M. The 2-1-1 board, participating with 3x cap, full pro-rata — we don't need super pro-rata — and the 2-year acceleration works. I think we can close this."},
    ]

    smart_final = {
        "Pre-Money Valuation": "$40M",
        "Board Composition": "2 founder, 1 investor, 1 independent",
        "Liquidation Preference": "1x participating, 3x cap",
        "Pro-Rata Rights": "Full pro-rata + super pro-rata",
        "Founder Vesting": "2-year acceleration, remaining vests",
    }
    smart_a, smart_b = case.score_deal(smart_final)
    smart_result = {
        "round_data": smart_rounds,
        "final_deal": smart_final,
        "final_scores": {"party_a_score": smart_a, "party_b_score": smart_b},
        "transcript": smart_transcript,
    }

    # ── BOTH SMART ──
    # Both parties use strategic iso-utility offers.
    # They quickly find efficient trades and reach a Pareto-optimal deal.
    both_rounds = [
        make_round(1, case.party_a_name, {
            "Pre-Money Valuation": "$40M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x non-participating",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "No reset, full credit for time served",
        }, case),
        make_round(1, case.party_b_name, {
            "Pre-Money Valuation": "$30M",
            "Board Composition": "2 founder, 2 investor, 1 independent",
            "Liquidation Preference": "1x participating",
            "Pro-Rata Rights": "Full pro-rata rights",
            "Founder Vesting": "3-year reset, 1-year cliff",
        }, case),
        make_round(2, case.party_a_name, {
            "Pre-Money Valuation": "$35M",
            "Board Composition": "2 founder, 1 investor, 0 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "No reset, full credit for time served",
        }, case),
        make_round(2, case.party_b_name, {
            "Pre-Money Valuation": "$35M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
        make_round(3, case.party_a_name, {
            "Pre-Money Valuation": "$35M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
        make_round(3, case.party_b_name, {
            "Pre-Money Valuation": "$35M",
            "Board Composition": "2 founder, 1 investor, 1 independent",
            "Liquidation Preference": "1x participating, 3x cap",
            "Pro-Rata Rights": "Full pro-rata + super pro-rata",
            "Founder Vesting": "2-year acceleration, remaining vests",
        }, case),
    ]

    both_transcript = [
        {"speaker": case.party_a_name, "message": "Morgan, here are three packages that work equally well for us — pick whichever fits your fund best. Package A: $40M, 2-1-1 board, non-participating, super pro-rata, full vesting credit. Package B: $35M, 2-1-0 board, participating capped at 3x, super pro-rata, full vesting credit."},
        {"speaker": case.party_b_name, "message": "Smart approach, Sam. Let me reciprocate. Two packages that are equivalent for us: Package X: $30M, 2-2-1 board, full participating, full pro-rata, 3-year reset. Package Y: $35M, 2-1-1 board, participating with 3x cap, super pro-rata, 2-year acceleration. Package Y clearly has overlap with your B."},
        {"speaker": case.party_a_name, "message": "Agreed — Package Y from you and Package B from me are converging. Let me refine: $35M, 2-1-1 board, participating with 3x cap, super pro-rata, full vesting credit. That gives you the governance and protection you need while preserving our vesting."},
        {"speaker": case.party_b_name, "message": "Very close. I can do $35M, 2-1-1 board, participating with 3x cap, and super pro-rata. On vesting, the 2-year acceleration with remaining shares vesting is my compromise — it's better than a full reset. This deal scores well for both of us."},
        {"speaker": case.party_a_name, "message": "You're right — the 2-year acceleration is reasonable and the rest of this package is strong. $35M, 2-1-1 board, participating preferred with 3x cap, super pro-rata, 2-year acceleration. Deal."},
        {"speaker": case.party_b_name, "message": "Deal. This is a package where neither of us is leaving value on the table. Let's get the lawyers drafting."},
    ]

    both_final = {
        "Pre-Money Valuation": "$35M",
        "Board Composition": "2 founder, 1 investor, 1 independent",
        "Liquidation Preference": "1x participating, 3x cap",
        "Pro-Rata Rights": "Full pro-rata + super pro-rata",
        "Founder Vesting": "2-year acceleration, remaining vests",
    }
    both_a, both_b = case.score_deal(both_final)
    both_result = {
        "round_data": both_rounds,
        "final_deal": both_final,
        "final_scores": {"party_a_score": both_a, "party_b_score": both_b},
        "transcript": both_transcript,
    }

    # ── Perspective data ──
    print("Computing perspective data...")
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

    demo_data = {
        "case_title": case.title,
        "party_a_name": case.party_a_name,
        "party_b_name": case.party_b_name,
        "party_a_batna_score": case.party_a_batna_score,
        "party_b_batna_score": case.party_b_batna_score,
        "frontier": frontier_points,
        "deal_cloud": deal_cloud,
        "naive": naive_result,
        "smart": smart_result,
        "both_smart": both_result,
        "party_a_view": {
            "label": f"{case.party_a_name}'s Map",
            "description": f"What {case.party_a_name.split(' ')[0]} thinks the deal space looks like",
            "deal_cloud": compute_deal_cloud(case_a_view),
            "frontier": compute_frontier_points(case_a_view),
        },
        "party_b_view": {
            "label": f"{case.party_b_name}'s Map",
            "description": f"What {case.party_b_name.split(' ')[0]} thinks the deal space looks like",
            "deal_cloud": compute_deal_cloud(case_b_view),
            "frontier": compute_frontier_points(case_b_view),
        },
    }

    # Re-score trajectories for each perspective
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
    print(f"  Both smart rounds: {len(both_result['round_data'])}")
    print(f"  Naive final: A={naive_a}, B={naive_b}, Joint={naive_a+naive_b}")
    print(f"  Smart final: A={smart_a}, B={smart_b}, Joint={smart_a+smart_b}")
    print(f"  Both final: A={both_a}, B={both_b}, Joint={both_a+both_b}")


if __name__ == "__main__":
    main()
