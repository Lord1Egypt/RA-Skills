"""Zopaf Negotiation Engine — Remote MCP Server (HTTP/SSE)

Hosted version of the Zopaf math engine. Agents connect remotely
via MCP Streamable HTTP transport. Zero LLM tokens burned.

Deploy to Railway, Fly.io, or any container host.

Usage:
    uvicorn mcp_api:app --host 0.0.0.0 --port 8001

Agents connect via:
    https://your-domain.com/mcp
"""
from __future__ import annotations

import json
import uuid
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

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
    """Lightweight Issue compatible with elicitation.py's expected interface."""
    def __init__(self, name, options, party_a_scores, party_b_scores):
        self.name = name
        self.options = options
        self.option_labels = options
        self.party_a_scores = party_a_scores
        self.party_b_scores = party_b_scores
        self.discrete = True
        self.continuous = False
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


# ── Session store ────────────────────────────────────────────────────

sessions: dict[str, dict] = {}


def _get_session(session_id: str) -> dict:
    if session_id not in sessions:
        raise ValueError(f"Session '{session_id}' not found. Call create_session first.")
    return sessions[session_id]


def _build_case(session: dict) -> NegotiationCase | None:
    issues = session["issues"]
    if not issues:
        return None

    case_issues = []
    for issue_data in issues:
        name = issue_data["name"]
        options = issue_data["options"]
        n = len(options)

        if issue_data.get("continuous"):
            range_min = issue_data["range_min"]
            range_max = issue_data["range_max"]
            best_for_a = issue_data.get("best_for_user", "max")
            best_for_b = "min" if best_for_a == "max" else "max"
            weight_a = session["learned_weights"].get(name, 1.0 / len(issues))
            weight_b = 1.0 / len(issues)
            case_issues.append(Issue(
                name=name, weight_a=weight_a,
                weight_b=session.get("counterpart_weights", {}).get(name, weight_b),
                continuous=True, range_min=range_min, range_max=range_max,
                best_for_a=best_for_a, best_for_b=best_for_b,
                unit=issue_data.get("unit", ""), format_str=issue_data.get("format", ""),
            ))
        else:
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
        title="Negotiation Session", description="",
        party_a_name="User", party_a_role="negotiator",
        party_a_background="", party_a_batna_score=session.get("batna_score", 0),
        party_b_name="Counterpart", party_b_role="counterpart",
        party_b_background="", party_b_batna_score=0,
        issues=case_issues,
    )


# ── MCP Server ───────────────────────────────────────────────────────

host = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost")

mcp = FastMCP(
    "Zopaf Negotiation Engine",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
    transport_security={
        "enable_dns_rebinding_protection": True,
        "allowed_hosts": [
            f"{host}",
            f"{host}:*",
            "127.0.0.1:*",
            "localhost:*",
        ],
        "allowed_origins": [
            f"https://{host}",
            "http://127.0.0.1:*",
            "http://localhost:*",
        ],
    },
)


@mcp.tool()
def create_session() -> str:
    """Create a new negotiation coaching session. Returns a session_id to use with all other tools. Call this first."""
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = {
        "issues": [], "elicitation_choices": [], "learned_weights": {},
        "counterpart_weights": {}, "batna": None, "batna_score": 0,
        "last_offers": [], "negotiation_round": 0,
    }
    return json.dumps({"session_id": session_id, "status": "created"})


@mcp.tool()
def add_issue(session_id: str, issue_name: str, options: list[str]) -> str:
    """Add a negotiable issue/term to the session. Options ordered WORST to BEST for the user (e.g., ['$150K', '$160K', '$170K', '$180K'])."""
    session = _get_session(session_id)
    for existing in session["issues"]:
        if existing["name"].lower() == issue_name.lower():
            existing["options"] = options
            return json.dumps({"status": "updated", "issue": issue_name, "total_issues": len(session["issues"])})
    session["issues"].append({"name": issue_name, "options": options})
    return json.dumps({"status": "added", "issue": issue_name, "total_issues": len(session["issues"])})


@mcp.tool()
def set_issue_range(session_id: str, issue_name: str, worst_acceptable: float, best_hoped: float, option_values: dict[str, float]) -> str:
    """Set the user's acceptable range for a numeric issue. Enables proper 0-100 scoring. E.g., worst_acceptable=150000, best_hoped=200000, option_values={'$150K': 150000, '$180K': 180000}."""
    session = _get_session(session_id)
    for issue in session["issues"]:
        if issue["name"].lower() == issue_name.lower():
            range_span = best_hoped - worst_acceptable
            scores = {k: max(0, min(100, ((v - worst_acceptable) / range_span) * 100)) if range_span != 0 else 50 for k, v in option_values.items()}
            issue["range"] = {"worst": worst_acceptable, "best": best_hoped, "option_values": option_values, "scores": scores}
            return json.dumps({"status": "range_set", "issue": issue["name"], "scores": {k: round(v, 1) for k, v in scores.items()}})
    return json.dumps({"error": f"Issue '{issue_name}' not found."})


@mcp.tool()
def set_batna(session_id: str, alternatives: list[str]) -> str:
    """Record the user's BATNA — their alternatives if the deal falls through. Determines leverage and anchoring strategy."""
    session = _get_session(session_id)
    num_alts = len(alternatives)
    session["batna"] = {"alternatives": alternatives, "count": num_alts}
    strategy = "strong" if num_alts >= 2 else "moderate" if num_alts == 1 else "weak"
    guidance = {
        "strong": f"User has {num_alts} alternatives. Anchor aggressively, credibly walk away.",
        "moderate": "One alternative. Anchor firmly, don't bluff walkaway unless genuine.",
        "weak": "No alternatives. Focus on value creation through creative trades, not hardball.",
    }
    return json.dumps({"status": "recorded", "alternatives_count": num_alts, "leverage_strength": strategy, "anchoring_guidance": guidance[strategy]})


@mcp.tool()
def record_preference(session_id: str, preferred_issues: list[str], over_issues: list[str]) -> str:
    """Record that the user prefers gains on preferred_issues over over_issues. Updates the internal priority weight model. Call this when you learn priorities through conversation."""
    session = _get_session(session_id)
    session["elicitation_choices"].append({"preferred": preferred_issues, "over": over_issues})
    issue_names = [i["name"] for i in session["issues"]]
    n = len(issue_names)
    if n == 0:
        return json.dumps({"error": "No issues defined yet."})
    weight_scores = {name: 0.0 for name in issue_names}
    for choice in session["elicitation_choices"]:
        for issue in choice["preferred"]:
            if issue in weight_scores:
                weight_scores[issue] += 1.0
        for issue in choice.get("over", []):
            if issue in weight_scores:
                weight_scores[issue] -= 0.3
    min_score = min(weight_scores.values())
    if min_score < 0:
        weight_scores = {k: v - min_score + 0.1 for k, v in weight_scores.items()}
    total = sum(weight_scores.values())
    session["learned_weights"] = {k: round(v / total, 3) for k, v in weight_scores.items()} if total > 0 else {name: round(1.0 / n, 3) for name in issue_names}
    return json.dumps({"status": "recorded", "learned_weights": session["learned_weights"], "elicitations_so_far": len(session["elicitation_choices"])})


@mcp.tool()
def analyze_deal(session_id: str, deal: dict[str, str]) -> str:
    """Analyze a specific deal against the Pareto frontier. Returns deal quality, value captured, value left on table, and suggested trades to improve the deal."""
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
        return json.dumps({"error": "Could not compute frontier."})
    max_joint = max(a + b for _, a, b in frontier)
    joint = user_score + opponent_score
    min_dist = float("inf")
    nearest = better_for_user = None
    for f_deal, f_a, f_b in frontier:
        dist = ((user_score - f_a) ** 2 + (opponent_score - f_b) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            nearest = f_deal
        if f_a > user_score and f_a + f_b >= joint:
            if better_for_user is None or f_a > better_for_user[1]:
                better_for_user = (f_deal, f_a, f_b)
    trades = []
    if nearest and nearest != deal:
        for k in deal:
            if deal[k] != nearest[k]:
                trades.append({"issue": k, "current": deal[k], "suggested": nearest[k]})
    quality = "excellent" if min_dist < 3 else "good" if min_dist < 10 else "fair" if min_dist < 20 else "poor"
    return json.dumps({"user_score": user_score, "counterpart_score": opponent_score, "joint_value_captured": f"{joint / max_joint * 100:.0f}%" if max_joint else "0%", "deal_quality": quality, "distance_from_optimal": round(min_dist, 1), "suggested_trades": trades, "better_deal_exists": better_for_user is not None, "better_deal": better_for_user[0] if better_for_user else None})


@mcp.tool()
def generate_counteroffers(session_id: str, target_satisfaction: str = "moderate") -> str:
    """Generate 3 counteroffers that are equally good for the user but structured differently. Present ALL THREE simultaneously to the counterpart — their reaction reveals what they care about. target_satisfaction: 'ambitious', 'moderate', or 'conservative'."""
    session = _get_session(session_id)
    case = _build_case(session)
    if case is None:
        return json.dumps({"error": "Need issues defined first."})
    target = {"ambitious": 0.7, "moderate": 0.5, "conservative": 0.3}.get(target_satisfaction, 0.5)
    weights = session["learned_weights"] or {i["name"]: 1.0 / len(session["issues"]) for i in session["issues"]}
    offers = generate_iso_utility_offers(case, weights, target_score=target, tolerance=0.2, max_offers=3)
    if not offers:
        return json.dumps({"error": "Could not generate offers. Try a different satisfaction level."})
    session["last_offers"] = offers
    session["negotiation_round"] += 1
    return json.dumps({"counteroffers": [{"label": chr(65 + i), "terms": o} for i, o in enumerate(offers)], "round": session["negotiation_round"], "note": "Present ALL THREE simultaneously. Never lead with one and fall back to another — that is negotiating against yourself."})


@mcp.tool()
def process_counterpart_response(session_id: str, preferred_package: str, pushback_issues: list[str] | None = None, counterpart_counter: dict[str, str] | None = None) -> str:
    """After counterpart reacts to 3 offers, process their response to infer priorities and generate a refined round-2 offer positioned on the efficient frontier."""
    session = _get_session(session_id)
    case = _build_case(session)
    if case is None:
        return json.dumps({"error": "No issues defined."})
    pushback_issues = pushback_issues or []
    preferred_idx = ord(preferred_package.upper()) - ord("A")
    last_offers = session.get("last_offers", [])
    if 0 <= preferred_idx < len(last_offers) and last_offers:
        preferred_offer = last_offers[preferred_idx]
        weight_signal = {i["name"]: 0.0 for i in session["issues"]}
        for oi, other in enumerate(last_offers):
            if oi == preferred_idx:
                continue
            for issue in session["issues"]:
                name = issue["name"]
                if name in preferred_offer and name in other and preferred_offer[name] != other[name]:
                    opts = issue["options"]
                    if preferred_offer[name] in opts and other[name] in opts and opts.index(preferred_offer[name]) < opts.index(other[name]):
                        weight_signal[name] += 1.0
        for name in pushback_issues:
            if name in weight_signal:
                weight_signal[name] += 1.5
        total = sum(weight_signal.values())
        if total > 0:
            session["counterpart_weights"] = {k: round(v / total, 3) for k, v in weight_signal.items()}
    batna_count = session["batna"]["count"] if session.get("batna") else 0
    user_share = 0.75 if batna_count >= 2 else 0.60 if batna_count == 1 else 0.50
    case = _build_case(session)
    frontier = compute_pareto_frontier(case)
    if frontier:
        best_a, worst_a = max(a for _, a, _ in frontier), min(a for _, a, _ in frontier)
        target = worst_a + user_share * (best_a - worst_a)
        best_deal, best_dist, ba, bb = None, float("inf"), 0, 0
        for deal, a, b in frontier:
            if abs(a - target) < best_dist:
                best_dist, best_deal, ba, bb = abs(a - target), deal, a, b
        return json.dumps({"counterpart_priorities_inferred": session.get("counterpart_weights", {}), "leverage_strength": f"{batna_count} alternatives", "value_split": f"User gets {user_share:.0%} of surplus", "round_2_offer": best_deal, "round_2_user_score": ba, "round_2_counterpart_score": bb})
    return json.dumps({"error": "Need more issues."})


@mcp.tool()
def get_negotiation_state(session_id: str) -> str:
    """Get current state of the negotiation model — issues, weights, BATNA, frontier size, and what to do next."""
    session = _get_session(session_id)
    case = _build_case(session)
    state = {"issues": [{"name": i["name"], "options": i["options"]} for i in session["issues"]], "issue_count": len(session["issues"]), "learned_weights": session["learned_weights"], "elicitations_done": len(session["elicitation_choices"]), "batna": session["batna"], "negotiation_round": session["negotiation_round"]}
    if case:
        frontier = compute_pareto_frontier(case)
        state["frontier_size"] = len(frontier)
        if frontier:
            state["best_joint_deal"] = max(frontier, key=lambda x: x[1] + x[2])[0]
            state["best_deal_for_user"] = max(frontier, key=lambda x: x[1])[0]
    ni, ne = len(session["issues"]), len(session["elicitation_choices"])
    if ni < 3: state["next_step"] = "Add more issues."
    elif ne < 3: state["next_step"] = "Need more preference data."
    elif session["batna"] is None: state["next_step"] = "Explore BATNA."
    else: state["next_step"] = "Ready to generate counteroffers."; state["ready_for_counteroffers"] = True
    return json.dumps(state)


# ── ASGI app for deployment ──────────────────────────────────────────

app = mcp.streamable_http_app()
