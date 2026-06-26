"""Zopaf Negotiation Engine — MCP Server

Exposes the Zopaf negotiation math engine as MCP tools that any
LLM agent can call. Zero LLM tokens burned — pure MILP optimization,
Pareto frontier analysis, and preference weight solving.

The calling agent handles conversation; Zopaf handles the math.

Usage:
    # stdio transport (for Claude Code, Claude Desktop, etc.)
    python3 zopaf_mcp_server.py

    # Or add to Claude Desktop config:
    # "zopaf": {
    #   "command": "python3",
    #   "args": ["/path/to/zopaf_mcp_server.py"]
    # }
"""
from __future__ import annotations

import json
import uuid
from typing import Any

from mcp.server.fastmcp import FastMCP

# ── Import the math engine (no Claude dependency) ────────────────────
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from case import NegotiationCase, Issue
from elicitation import (
    compute_weighted_score,
    generate_iso_utility_offers,
    solve_weights,
)
from scorer import (
    compute_pareto_frontier,
    compute_anti_frontier,
    analyze_outcome,
)


class SimpleIssue:
    """Lightweight Issue compatible with elicitation.py's expected interface.
    elicitation.py expects .name, .options (list), not .option_labels."""
    def __init__(self, name, options, party_a_scores, party_b_scores):
        self.name = name
        self.options = options
        self.option_labels = options  # alias for scorer compat
        self.party_a_scores = party_a_scores
        self.party_b_scores = party_b_scores
        self.discrete = True
        self.continuous = False
        # Compute satisfaction/weights for scorer.py compat
        a_vals = list(party_a_scores.values())
        b_vals = list(party_b_scores.values())
        a_min, a_max = min(a_vals), max(a_vals)
        b_min, b_max = min(b_vals), max(b_vals)
        a_range = a_max - a_min if a_max != a_min else 1
        b_range = b_max - b_min if b_max != b_min else 1
        self.satisfaction_a = {o: (party_a_scores[o] - a_min) / a_range for o in options}
        self.satisfaction_b = {o: (party_b_scores[o] - b_min) / b_range for o in options}
        self.weight_a = 0.0
        self.weight_b = 0.0

    def get_satisfaction(self, value):
        label = str(value)
        return self.satisfaction_a.get(label, 0.0), self.satisfaction_b.get(label, 0.0)

    def score(self, value):
        sa, sb = self.get_satisfaction(value)
        return sa * self.weight_a, sb * self.weight_b

# ── MCP Server ───────────────────────────────────────────────────────

mcp = FastMCP("Zopaf Negotiation Engine")

# In-memory session store (swap for Redis/SQLite in production)
sessions: dict[str, dict] = {}


def _get_session(session_id: str) -> dict:
    if session_id not in sessions:
        raise ValueError(f"Session '{session_id}' not found. Call create_session first.")
    return sessions[session_id]


def _build_case(session: dict) -> NegotiationCase | None:
    """Build a NegotiationCase from session state. Pure math, no LLM."""
    issues = session["issues"]
    if not issues:
        return None

    case_issues = []
    for issue_data in issues:
        name = issue_data["name"]
        options = issue_data["options"]
        n = len(options)

        if issue_data.get("continuous"):
            # Continuous issue
            range_min = issue_data["range_min"]
            range_max = issue_data["range_max"]
            best_for_a = issue_data.get("best_for_user", "max")
            # Assume counterpart prefers opposite
            best_for_b = "min" if best_for_a == "max" else "max"
            weight_a = session["learned_weights"].get(name, 1.0 / len(issues))
            weight_b = 1.0 / len(issues)  # default counterpart weight

            case_issues.append(Issue(
                name=name,
                weight_a=weight_a,
                weight_b=session.get("counterpart_weights", {}).get(name, weight_b),
                continuous=True,
                range_min=range_min,
                range_max=range_max,
                best_for_a=best_for_a,
                best_for_b=best_for_b,
                unit=issue_data.get("unit", ""),
                format_str=issue_data.get("format", ""),
            ))
        else:
            # Discrete issue
            user_scores = {}
            opponent_scores = {}

            if "range" in issue_data:
                range_scores = issue_data["range"]["scores"]
                for opt in options:
                    matched_score = None
                    for range_opt, score in range_scores.items():
                        if range_opt.lower() == opt.lower() or range_opt in opt or opt in range_opt:
                            matched_score = score
                            break
                    if matched_score is not None:
                        user_scores[opt] = round(matched_score)
                    else:
                        idx = options.index(opt)
                        user_scores[opt] = round(idx / max(1, n - 1) * 100) if n > 1 else 50
                    opponent_scores[opt] = 100 - user_scores[opt]
            else:
                for i, opt in enumerate(options):
                    user_scores[opt] = i * (40 // max(1, n - 1)) if n > 1 else 20
                    opponent_scores[opt] = (n - 1 - i) * (40 // max(1, n - 1)) if n > 1 else 20

            weight_a = session["learned_weights"].get(name, 1.0 / len(issues))
            weight_b = session.get("counterpart_weights", {}).get(name, 1.0 / len(issues))

            si = SimpleIssue(name, options, user_scores, opponent_scores)
            si.weight_a = weight_a
            si.weight_b = weight_b
            case_issues.append(si)

    return NegotiationCase(
        title="Negotiation Session",
        description="",
        party_a_name="User",
        party_a_role="negotiator",
        party_a_background="",
        party_a_batna_score=session.get("batna_score", 0),
        party_b_name="Counterpart",
        party_b_role="counterpart",
        party_b_background="",
        party_b_batna_score=0,
        issues=case_issues,
    )


# ── MCP Tools ────────────────────────────────────────────────────────

@mcp.tool()
def create_session() -> str:
    """Create a new negotiation coaching session. Returns a session_id
    to use with all other tools. Call this first before any other tool."""
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = {
        "issues": [],
        "elicitation_choices": [],
        "learned_weights": {},
        "counterpart_weights": {},
        "batna": None,
        "batna_score": 0,
        "last_offers": [],
        "negotiation_round": 0,
    }
    return json.dumps({"session_id": session_id, "status": "created"})


@mcp.tool()
def add_issue(
    session_id: str,
    issue_name: str,
    options: list[str],
) -> str:
    """Add a negotiable issue/term to the session.

    Args:
        session_id: Session ID from create_session
        issue_name: Name of the issue (e.g., 'Salary', 'Equity', 'Start Date')
        options: Possible options ordered WORST to BEST for the user
                 (e.g., ['$150K', '$160K', '$170K', '$180K'])
    """
    session = _get_session(session_id)

    issue = {"name": issue_name, "options": options}

    # Check for duplicates — update if exists
    for existing in session["issues"]:
        if existing["name"].lower() == issue_name.lower():
            existing["options"] = options
            return json.dumps({
                "status": "updated",
                "issue": issue_name,
                "options": options,
                "total_issues": len(session["issues"]),
            })

    session["issues"].append(issue)
    return json.dumps({
        "status": "added",
        "issue": issue_name,
        "options": options,
        "total_issues": len(session["issues"]),
    })


@mcp.tool()
def set_issue_range(
    session_id: str,
    issue_name: str,
    worst_acceptable: float,
    best_hoped: float,
    option_values: dict[str, float],
) -> str:
    """Set the user's acceptable range for a numeric issue, enabling
    proper 0-100 scoring based on where each option falls in the range.

    Args:
        session_id: Session ID
        issue_name: Must match an existing issue from add_issue
        worst_acceptable: Floor value (maps to score 0). E.g., salary: 150000
        best_hoped: Target value (maps to score 100). E.g., salary: 200000
        option_values: Map option name -> numeric value.
                       E.g., {'$150K': 150000, '$180K': 180000}
    """
    session = _get_session(session_id)

    for issue in session["issues"]:
        if issue["name"].lower() == issue_name.lower():
            range_span = best_hoped - worst_acceptable
            scores = {}
            for opt_name, opt_val in option_values.items():
                if range_span != 0:
                    scores[opt_name] = max(0, min(100, ((opt_val - worst_acceptable) / range_span) * 100))
                else:
                    scores[opt_name] = 50
            issue["range"] = {
                "worst": worst_acceptable,
                "best": best_hoped,
                "option_values": option_values,
                "scores": scores,
            }
            return json.dumps({
                "status": "range_set",
                "issue": issue["name"],
                "scores": {k: round(v, 1) for k, v in scores.items()},
            })

    return json.dumps({"error": f"Issue '{issue_name}' not found. Add it first with add_issue."})


@mcp.tool()
def set_batna(
    session_id: str,
    alternatives: list[str],
) -> str:
    """Record the user's BATNA — their alternatives if the deal falls through.
    The number and quality of alternatives determines anchoring strategy.

    Args:
        session_id: Session ID
        alternatives: List of alternatives (e.g., ['competing offer from Company B at $165K',
                      'stay in current role']). Empty list if no alternatives.
    """
    session = _get_session(session_id)
    num_alts = len(alternatives)

    session["batna"] = {"alternatives": alternatives, "count": num_alts}

    if num_alts >= 2:
        strategy = "strong"
        guidance = (
            f"User has {num_alts} alternatives. They can anchor aggressively and "
            "credibly walk away. Recommend making the first offer to set the anchor."
        )
    elif num_alts == 1:
        strategy = "moderate"
        guidance = (
            "User has one alternative. Anchor firmly but don't bluff a walkaway "
            "unless genuinely willing to take it."
        )
    else:
        strategy = "weak"
        guidance = (
            "No concrete alternatives. Focus on value creation through creative "
            "trades rather than hardball. Use market benchmarks to anchor."
        )

    return json.dumps({
        "status": "recorded",
        "alternatives_count": num_alts,
        "leverage_strength": strategy,
        "anchoring_guidance": guidance,
    })


@mcp.tool()
def record_preference(
    session_id: str,
    preferred_issues: list[str],
    over_issues: list[str],
) -> str:
    """Record that the user prefers gains on some issues over others.
    This updates the internal weight model. Call this when you learn
    the user's priorities through conversation or direct questions.

    Args:
        session_id: Session ID
        preferred_issues: Issues the user prioritizes (e.g., ['Salary', 'Equity'])
        over_issues: Issues the user would trade away (e.g., ['Start Date', 'Title'])
    """
    session = _get_session(session_id)

    session["elicitation_choices"].append({
        "preferred": preferred_issues,
        "over": over_issues,
    })

    # Recompute weights from all accumulated preferences
    issue_names = [i["name"] for i in session["issues"]]
    n = len(issue_names)
    if n == 0:
        return json.dumps({"error": "No issues defined yet."})

    weight_scores = {name: 0.0 for name in issue_names}
    for choice in session["elicitation_choices"]:
        for issue in choice["preferred"]:
            if issue in weight_scores:
                weight_scores[issue] += 1.0
        # Issues traded away get slight negative signal
        for issue in choice.get("over", []):
            if issue in weight_scores:
                weight_scores[issue] -= 0.3

    # Shift to positive and normalize
    min_score = min(weight_scores.values())
    if min_score < 0:
        weight_scores = {k: v - min_score + 0.1 for k, v in weight_scores.items()}

    total = sum(weight_scores.values())
    if total > 0:
        session["learned_weights"] = {k: round(v / total, 3) for k, v in weight_scores.items()}
    else:
        session["learned_weights"] = {name: round(1.0 / n, 3) for name in issue_names}

    return json.dumps({
        "status": "recorded",
        "learned_weights": session["learned_weights"],
        "elicitations_so_far": len(session["elicitation_choices"]),
    })


@mcp.tool()
def analyze_deal(
    session_id: str,
    deal: dict[str, str],
) -> str:
    """Analyze a specific deal against the Pareto frontier. Returns how
    good the deal is, how much value is left on the table, and what
    trades could improve it.

    Args:
        session_id: Session ID
        deal: Map of issue_name -> chosen option (e.g., {'Salary': '$170K', 'Equity': '0.5%'})
    """
    session = _get_session(session_id)
    case = _build_case(session)
    if case is None:
        return json.dumps({"error": "No issues defined yet."})

    missing = [i["name"] for i in session["issues"] if i["name"] not in deal]
    if missing:
        return json.dumps({"error": f"Deal missing issues: {missing}"})

    user_score, opponent_score = case.score_deal(deal)
    frontier = compute_pareto_frontier(case)

    if not frontier:
        return json.dumps({"error": "Could not compute frontier. Need more issues."})

    max_joint = max(a + b for _, a, b in frontier)
    joint = user_score + opponent_score
    value_pct = (joint / max_joint * 100) if max_joint > 0 else 0

    # Find nearest frontier deal
    min_dist = float("inf")
    nearest = None
    better_for_user = None
    for f_deal, f_a, f_b in frontier:
        dist = ((user_score - f_a) ** 2 + (opponent_score - f_b) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            nearest = f_deal
        if f_a > user_score and f_a + f_b >= joint:
            if better_for_user is None or f_a > better_for_user[1]:
                better_for_user = (f_deal, f_a, f_b)

    # Find tradeable improvements
    trade_suggestions = []
    if nearest and nearest != deal:
        for issue_name in deal:
            if deal[issue_name] != nearest[issue_name]:
                trade_suggestions.append({
                    "issue": issue_name,
                    "current": deal[issue_name],
                    "suggested": nearest[issue_name],
                })

    return json.dumps({
        "user_score": user_score,
        "counterpart_score": opponent_score,
        "joint_score": joint,
        "max_possible_joint": max_joint,
        "joint_value_captured": f"{value_pct:.0f}%",
        "distance_from_optimal": round(min_dist, 1),
        "deal_quality": (
            "excellent" if min_dist < 3 else
            "good" if min_dist < 10 else
            "fair" if min_dist < 20 else
            "poor — significant value left on the table"
        ),
        "suggested_trades": trade_suggestions,
        "better_deal_exists": better_for_user is not None,
        "better_deal": better_for_user[0] if better_for_user else None,
    })


@mcp.tool()
def generate_counteroffers(
    session_id: str,
    target_satisfaction: str = "moderate",
) -> str:
    """Generate 3 counter-offers that are equally good for the user but
    structured differently. Present ALL THREE simultaneously to the
    counterpart — their reaction reveals their priorities.

    Args:
        session_id: Session ID
        target_satisfaction: How aggressively to position offers.
                            'ambitious' (user-favoring), 'moderate', or 'conservative'
    """
    session = _get_session(session_id)
    case = _build_case(session)
    if case is None:
        return json.dumps({"error": "Need issues defined first."})

    target_map = {"ambitious": 0.7, "moderate": 0.5, "conservative": 0.3}
    target = target_map.get(target_satisfaction, 0.5)

    weights = session["learned_weights"] if session["learned_weights"] else {
        issue["name"]: 1.0 / len(session["issues"]) for issue in session["issues"]
    }

    offers = generate_iso_utility_offers(
        case, weights, target_score=target, tolerance=0.2, max_offers=3,
    )

    if not offers:
        return json.dumps({"error": "Could not generate offers at this level. Try a different satisfaction level."})

    session["last_offers"] = offers
    session["negotiation_round"] += 1

    formatted = [{"label": chr(65 + i), "terms": offer} for i, offer in enumerate(offers)]

    return json.dumps({
        "counteroffers": formatted,
        "round": session["negotiation_round"],
        "note": (
            "Present ALL THREE simultaneously. The counterpart's preference "
            "reveals their priorities. Never 'lead with A, fall back to B' — "
            "that is negotiating against yourself."
        ),
    })


@mcp.tool()
def process_counterpart_response(
    session_id: str,
    preferred_package: str,
    pushback_issues: list[str] | None = None,
    counterpart_counter: dict[str, str] | None = None,
) -> str:
    """After the counterpart reacts to the 3 offers, process their response
    to infer their priorities and generate a refined round-2 offer.

    Args:
        session_id: Session ID
        preferred_package: Which package they preferred ('A', 'B', or 'C')
        pushback_issues: Issues they pushed back on (optional)
        counterpart_counter: Any counter-offer terms they proposed (optional)
    """
    session = _get_session(session_id)
    case = _build_case(session)
    if case is None:
        return json.dumps({"error": "No issues defined."})

    pushback_issues = pushback_issues or []
    counterpart_counter = counterpart_counter or {}

    preferred_idx = ord(preferred_package.upper()) - ord("A")
    last_offers = session.get("last_offers", [])

    if 0 <= preferred_idx < len(last_offers) and last_offers:
        preferred_offer = last_offers[preferred_idx]

        # Infer counterpart weights from preference
        weight_signal = {issue["name"]: 0.0 for issue in session["issues"]}
        for other_idx, other_offer in enumerate(last_offers):
            if other_idx == preferred_idx:
                continue
            for issue in session["issues"]:
                name = issue["name"]
                if name in preferred_offer and name in other_offer:
                    pref_opt = preferred_offer[name]
                    other_opt = other_offer[name]
                    if pref_opt != other_opt:
                        opts = issue["options"]
                        if pref_opt in opts and other_opt in opts:
                            if opts.index(pref_opt) < opts.index(other_opt):
                                weight_signal[name] += 1.0

        for issue_name in pushback_issues:
            if issue_name in weight_signal:
                weight_signal[issue_name] += 1.5

        total = sum(weight_signal.values())
        if total > 0:
            session["counterpart_weights"] = {k: round(v / total, 3) for k, v in weight_signal.items()}

    # BATNA-weighted split for round 2
    batna_count = session["batna"]["count"] if session.get("batna") else 0
    if batna_count >= 2:
        user_share = 0.75
    elif batna_count == 1:
        user_share = 0.60
    else:
        user_share = 0.50

    # Rebuild case with updated counterpart weights
    case = _build_case(session)
    frontier = compute_pareto_frontier(case)

    if frontier:
        best_for_user = max(a for _, a, _ in frontier)
        worst_for_user = min(a for _, a, _ in frontier)
        target_score = worst_for_user + user_share * (best_for_user - worst_for_user)

        best_deal = None
        best_dist = float("inf")
        best_a = best_b = 0
        for deal, a_score, b_score in frontier:
            dist = abs(a_score - target_score)
            if dist < best_dist:
                best_dist = dist
                best_deal = deal
                best_a = a_score
                best_b = b_score

        return json.dumps({
            "counterpart_priorities_inferred": session.get("counterpart_weights", {}),
            "leverage_strength": f"{batna_count} alternatives",
            "value_split": f"User gets {user_share:.0%} of surplus",
            "round_2_offer": best_deal,
            "round_2_user_score": best_a,
            "round_2_counterpart_score": best_b,
            "strategy": (
                f"Round 2 offer sits on the efficient frontier. Both sides improve "
                f"vs current position, but user captures {user_share:.0%} of the value "
                f"based on their leverage."
            ),
        })

    return json.dumps({"error": "Need more issues to compute frontier."})


@mcp.tool()
def get_negotiation_state(
    session_id: str,
) -> str:
    """Get the current state of the negotiation model — issues, weights,
    BATNA, frontier size, and strategic insights. Use this to understand
    where the negotiation stands and what to do next.

    Args:
        session_id: Session ID
    """
    session = _get_session(session_id)
    case = _build_case(session)

    state = {
        "issues": [{"name": i["name"], "options": i["options"]} for i in session["issues"]],
        "issue_count": len(session["issues"]),
        "learned_weights": session["learned_weights"],
        "elicitations_done": len(session["elicitation_choices"]),
        "batna": session["batna"],
        "negotiation_round": session["negotiation_round"],
        "counterpart_weights": session.get("counterpart_weights", {}),
    }

    if case:
        frontier = compute_pareto_frontier(case)
        state["frontier_size"] = len(frontier)

        if frontier:
            best_joint = max(frontier, key=lambda x: x[1] + x[2])
            best_for_user = max(frontier, key=lambda x: x[1])
            state["best_joint_deal"] = best_joint[0]
            state["best_deal_for_user"] = best_for_user[0]

        sorted_weights = sorted(session["learned_weights"].items(), key=lambda x: -x[1])
        state["priority_ranking"] = [k for k, v in sorted_weights]

    # Readiness assessment
    n_issues = len(session["issues"])
    n_elicit = len(session["elicitation_choices"])
    has_batna = session["batna"] is not None

    if n_issues < 3:
        state["next_step"] = "Add more issues — most negotiations have 5-10 terms. Surface the hidden ones."
    elif n_elicit < 3:
        state["next_step"] = "Need more preference data. Ask tradeoff questions to learn priorities."
    elif not has_batna:
        state["next_step"] = "Explore BATNA — what happens if the deal falls through?"
    else:
        state["next_step"] = "Ready to generate counteroffers."
        state["ready_for_counteroffers"] = True

    return json.dumps(state)


# ── Run ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
