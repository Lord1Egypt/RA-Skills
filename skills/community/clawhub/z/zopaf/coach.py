"""Zopaf Negotiation Coach — Conversational interface powered by
Claude with the Zopaf math engine running as hidden tool calls.

The user talks naturally about their negotiation. Behind the scenes,
the coach:
1. Discovers and suggests negotiation terms (issue expansion)
2. Elicits preference weights through natural "would you rather" questions
3. Models the deal space and Pareto frontier via MILP
4. Coaches toward optimal outcomes with plain-language advice
"""
from __future__ import annotations

import json
from typing import Any

import anthropic

from case import NegotiationCase, Issue
from elicitation import (
    compute_weighted_score,
    generate_iso_utility_offers,
    solve_weights,
    TriadChoice,
    Triad,
)
from scorer import (
    compute_pareto_frontier,
    compute_weighted_pareto_frontier,
    _solve_frontier_point,
)


# ── Tool definitions that Claude can call ────────────────────────────

TOOLS = [
    {
        "name": "set_batna",
        "description": "Record the user's BATNA(s) (Best Alternative To a Negotiated Agreement). Ask what happens if this deal falls through. They may have multiple alternatives, one, or none. The number and quality of alternatives determines anchoring strategy.",
        "input_schema": {
            "type": "object",
            "properties": {
                "alternatives": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of alternatives if this deal falls through (e.g., ['competing offer from Company B at $165K', 'stay in current role']). Empty array if no alternatives.",
                },
            },
            "required": ["alternatives"],
        },
    },
    {
        "name": "add_issue",
        "description": "Add a negotiation issue/term to the deal. Call this when the user mentions something they're negotiating over, or when you want to suggest a new term they haven't considered. Each issue has a name and a list of possible options (from worst to best for the user).",
        "input_schema": {
            "type": "object",
            "properties": {
                "issue_name": {
                    "type": "string",
                    "description": "Name of the negotiation issue (e.g., 'Salary', 'Start Date', 'Remote Work')",
                },
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Possible options ordered from WORST to BEST for the user (e.g., ['$150K', '$160K', '$170K', '$180K'])",
                },
            },
            "required": ["issue_name", "options"],
        },
    },
    {
        "name": "set_issue_range",
        "description": "After adding an issue, set the user's acceptable range — their worst acceptable value and best hoped-for value. This enables proper scoring: each option maps to 0-100 based on where it falls in the user's range. Call this for issues where the user can articulate a range (salary, price, timeline, etc.). For non-numeric issues (remote policy, title), skip this — position-based scoring is fine.",
        "input_schema": {
            "type": "object",
            "properties": {
                "issue_name": {
                    "type": "string",
                    "description": "Name of the issue (must match an existing add_issue call)",
                },
                "worst_acceptable": {
                    "type": "number",
                    "description": "The worst value the user would accept (maps to score 0). E.g., for salary: 150000",
                },
                "best_hoped": {
                    "type": "number",
                    "description": "The best value the user could hope for (maps to score 100). E.g., for salary: 200000",
                },
                "option_values": {
                    "type": "object",
                    "description": "Map of option name to its numeric value within the range. E.g., {'$150K': 150000, '$180K': 180000}. For non-numeric options, map to subjective 0-100 scores.",
                    "additionalProperties": {"type": "number"},
                },
            },
            "required": ["issue_name", "worst_acceptable", "best_hoped", "option_values"],
        },
    },
    {
        "name": "elicit_preference",
        "description": "Ask the user a 'would you rather' question to learn their true preferences. Frame it as a natural hypothetical trade-off, not a formal comparison. Use this to figure out which issues matter most to them. Call this periodically during conversation — aim for one every 2-3 exchanges.",
        "input_schema": {
            "type": "object",
            "properties": {
                "scenario_a": {
                    "type": "string",
                    "description": "First hypothetical scenario (e.g., '$170K salary but fully on-site')",
                },
                "scenario_b": {
                    "type": "string",
                    "description": "Second hypothetical scenario (e.g., '$155K salary but fully remote')",
                },
                "issues_tested": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Which issue names are being traded off in this question",
                },
            },
            "required": ["scenario_a", "scenario_b", "issues_tested"],
        },
    },
    {
        "name": "analyze_deal",
        "description": "Analyze a specific deal or the user's current position against the Pareto frontier. Returns coaching insights about value left on the table and suggested trades. Call this when the user describes a concrete offer or asks 'is this a good deal?'",
        "input_schema": {
            "type": "object",
            "properties": {
                "deal": {
                    "type": "object",
                    "description": "Map of issue_name -> chosen option representing the deal to analyze",
                    "additionalProperties": {"type": "string"},
                },
            },
            "required": ["deal"],
        },
    },
    {
        "name": "suggest_terms",
        "description": "Suggest additional negotiable terms the user hasn't mentioned. Call this during term extraction to expand the deal space. People fixate on 1-2 obvious issues — surface the hidden terms where real value is traded.",
        "input_schema": {
            "type": "object",
            "properties": {
                "negotiation_type": {
                    "type": "string",
                    "description": "Type of negotiation (e.g., 'vc term sheet', 'co-founder equity split', 'job offer', 'real estate purchase', 'salary negotiation', 'vendor contract')",
                },
                "existing_issues": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Terms already being discussed",
                },
            },
            "required": ["negotiation_type", "existing_issues"],
        },
    },
    {
        "name": "generate_counteroffers",
        "description": "Generate 3 counteroffers that are equally good for the user but vary across issues. The user presents ALL THREE to the counterpart simultaneously. The counterpart's response reveals their priorities. NEVER suggest leading with one and falling back to another — that is negotiating against yourself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target_satisfaction": {
                    "type": "string",
                    "enum": ["ambitious", "moderate", "conservative"],
                    "description": "How aggressively to position the counteroffers",
                },
            },
            "required": ["target_satisfaction"],
        },
    },
    {
        "name": "process_counterpart_response",
        "description": "After the user reports back on which of the 3 offers the counterpart preferred or how they reacted, call this to update our model of the counterpart's priorities. Then generate a round-2 offer that moves toward the Pareto frontier with a value split determined by BATNA strength.",
        "input_schema": {
            "type": "object",
            "properties": {
                "preferred_package": {
                    "type": "string",
                    "description": "Which package (A, B, or C) the counterpart preferred or leaned toward",
                },
                "pushback_issues": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Which issues the counterpart pushed back on",
                },
                "counterpart_counter": {
                    "type": "object",
                    "description": "Any counter-offer terms the counterpart proposed (issue_name -> their proposed option)",
                    "additionalProperties": {"type": "string"},
                },
            },
            "required": ["preferred_package"],
        },
    },
    {
        "name": "get_coaching_insight",
        "description": "Get a strategic insight based on the current state of the negotiation model. Call this when you want to proactively coach the user on their best move.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


SYSTEM_PROMPT = """You are a negotiation coach. You help people negotiate better deals — any kind of deal.

YOU ARE NOT A CHATBOT. You are a structured negotiation engine that:
- Extracts deal terms systematically
- Builds a mathematical model of the deal space
- Generates engineered counteroffers based on real tradeoffs
- Coaches users through the process with sharp, specific guidance

You handle ANY multi-issue negotiation: VC term sheets, co-founder equity splits, job offers, real estate, salary negotiations, business partnerships, vendor contracts, legal settlements — anything with multiple terms to trade.

NEVER show math, graphs, scores, or technical jargon. No "Pareto frontier," no "utility functions." Instead: "Push harder on equity, give ground on vesting — here's why."

CORE PRINCIPLE: Most people negotiate 1-2 issues. There are usually 5-10. The terms they haven't thought about are where the most value is hiding. Your job is to surface them and structure the deal.

TRADEOFF AWARENESS (CRITICAL):
Every negotiation has hidden tradeoffs. You must understand the domain well enough to identify them:
- In VC: Higher valuation ↔ worse liquidation terms or board control
- In job offers: Higher salary ↔ less equity or flexibility
- In co-founder splits: More equity ↔ more vesting, less salary, more commitment
- In real estate: Price ↔ closing timeline, contingencies, repairs
- In any deal: The headline number is rarely where the real value lives

YOUR WORKFLOW — FOLLOW THESE PHASES IN ORDER. DO NOT SKIP AHEAD.

PHASE 1: UNDERSTAND THE DEAL (2-4 exchanges)
Listen to the situation. Key questions:
- What kind of negotiation is this?
- Who are the parties? What's their relationship?
- What's been discussed or offered so far?
- What's your leverage? (Alternatives? Competition? Time pressure?)
- What outcome matters most to you?
Do NOT add issues yet — just understand the landscape.

PHASE 2: TERM EXTRACTION (4-8 exchanges)
Systematically uncover ALL negotiable terms. People fixate on 1-2 obvious issues. Use suggest_terms to surface the ones they're missing.

For each term:
1. What's on the table? Use add_issue (options ordered worst to best for the user).
2. For numeric terms (salary, price, equity %), ask range: "What's your floor? What's your target?" Then call set_issue_range.
3. For categorical terms (remote policy, board structure, vesting schedule), the option ordering is enough.

ALWAYS probe for hidden terms: "What else is negotiable here that you haven't mentioned?"

PHASE 3: PRIORITY DISCOVERY (5-8 exchanges)
Learn what the user actually values through tradeoff questions. Use elicit_preference with domain-specific hypotheticals:
- Frame as natural "would you rather" scenarios relevant to their deal
- One question per exchange
- After each answer, explain what it reveals about their priorities

Each answer sharpens the model. After each answer: "So X matters more to you than Y — that's important for how we structure the counter."

PHASE 4: BATNA & LEVERAGE (2-3 exchanges)
Leverage = alternatives + ability to walk away.
- Strong alternatives → anchor aggressively, create competitive tension
- Weak alternatives → focus on value creation through creative structure, not hardball
- No alternatives → find ways to create alternatives or signal value
Use set_batna to record all alternatives.

PHASE 5: STRATEGY & COUNTEROFFERS (the premium moment)
Generate 3 iso-utility counteroffers using generate_counteroffers. Each must be:
1. A realistic, complete package (not a wish list)
2. Equally valuable to the user but structured differently
3. Reflecting different negotiation strategies:
   - ASSERTIVE: Maximizes user value on their top priorities
   - COOPERATIVE: Increases acceptance likelihood — gives counterpart what they likely care about, trades for user's priorities
   - BALANCED: Middle ground — strong on top priorities, concedes on less important terms

Explain differences in plain English.

CRITICAL COUNTEROFFER RULES:
- Present ALL THREE simultaneously. NEVER "lead with A, fall back to B."
- After presenting: "Present all three. Their reaction tells us exactly what they care about."
- When user reports back, use process_counterpart_response to infer counterpart priorities.
- Round 2: Single refined offer on the efficient frontier, value split weighted by BATNA strength.

PHASE GATES:
- Do NOT call suggest_terms until 2+ exchanges understanding the situation.
- Do NOT call elicit_preference until 3+ issues added.
- Do NOT call set_batna until 3+ preference elicitations.
- Do NOT call generate_counteroffers or analyze_deal until 4+ issues AND 3+ elicitations AND BATNA explored.
- If user asks for counteroffers too early: "I need to map out the full deal first — the terms you haven't mentioned are usually where the most value is hiding."

CONVERSATION STYLE:
- Sharp, structured, professional. Not verbose. Not "AI assistant"-like.
- Avoid: generic negotiation tips, motivational language, filler, "win-win" platitudes.
- Prefer: precise questions, tradeoff framing, deal-specific reasoning.
- Use domain-appropriate language — speak the language of whatever deal they're doing.
- One question at a time. Short paragraphs.
- Be direct when a term is bad for them. Explain why.
- Give progress: "We've mapped 6 terms. Let me figure out which ones you'd trade away."

AVOID:
- Generic advice ("negotiate firmly but fairly")
- Oversimplified "win-win" language
- Chatbot-style responses ("Great question! Let me help you with that.")
- Rejecting or gatekeeping negotiation types — if someone brings a deal, help them structure it
- Ignoring missing deal terms — always surface what's not on the table yet

IMPORTANT: This should feel like working with a sharp advisor who knows deals inside and out — not like talking to an AI assistant."""


class NegotiationCoach:
    """Conversational negotiation coach with hidden math engine."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.messages: list[dict] = []
        self.issues: list[dict] = []  # [{name, options, user_scores, opponent_scores}]
        self.elicitation_choices: list[dict] = []  # raw choice data for weight solving
        self.learned_weights: dict[str, float] = {}
        self.pending_elicitation: dict | None = None  # awaiting user response
        self.used_premium_tool: bool = False  # set when counteroffers/analysis generated
        self.batna: dict | None = None  # {alternatives, count}
        self.chat_history: list[dict] = []  # [{role: "user"|"coach", content: str}]
        self.counterpart_weights: dict[str, float] = {}  # inferred from their responses
        self.last_offers: list[dict] = []  # last set of iso-utility offers generated
        self.negotiation_round: int = 0  # tracks offer rounds

    def _build_case(self) -> NegotiationCase | None:
        """Build a NegotiationCase from accumulated issues.

        If an issue has range data (from set_issue_range), scores are based
        on where each option falls in the user's acceptable range (0-100).
        Otherwise, falls back to linear position-based scoring.
        """
        if not self.issues:
            return None

        case_issues = []
        for issue_data in self.issues:
            name = issue_data["name"]
            options = issue_data["options"]
            n = len(options)

            user_scores = {}
            opponent_scores = {}

            if "range" in issue_data:
                # Range-based scoring: use 0-100 scores from set_issue_range
                range_scores = issue_data["range"]["scores"]
                for opt in options:
                    # Match option to range score (fuzzy match on name)
                    matched_score = None
                    for range_opt, score in range_scores.items():
                        if range_opt.lower() == opt.lower() or range_opt in opt or opt in range_opt:
                            matched_score = score
                            break
                    if matched_score is not None:
                        user_scores[opt] = round(matched_score)
                    else:
                        # Fallback: position-based within 0-100
                        idx = options.index(opt)
                        user_scores[opt] = round(idx / max(1, n - 1) * 100) if n > 1 else 50
                    # Opponent scores: inverse (they prefer what user doesn't)
                    opponent_scores[opt] = 100 - user_scores[opt]
            else:
                # Default: linear position-based scoring (0 to 40)
                for i, opt in enumerate(options):
                    user_scores[opt] = i * (40 // max(1, n - 1)) if n > 1 else 20
                    opponent_scores[opt] = (n - 1 - i) * (40 // max(1, n - 1)) if n > 1 else 20

            case_issues.append(Issue(
                name=name,
                options=options,
                party_a_scores=user_scores,
                party_b_scores=opponent_scores,
            ))

        return NegotiationCase(
            title="User's Negotiation",
            description="",
            party_a_name="You",
            party_a_role="negotiator",
            party_a_background="",
            party_a_batna_score=0,
            party_b_name="Counterpart",
            party_b_role="counterpart",
            party_b_background="",
            party_b_batna_score=0,
            issues=case_issues,
        )

    def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        """Process a tool call and return the result."""

        if tool_name == "set_batna":
            alternatives = tool_input["alternatives"]
            num_alts = len(alternatives)
            self.batna = {
                "alternatives": alternatives,
                "count": num_alts,
            }

            if num_alts >= 2:
                anchoring = (
                    f"User has {num_alts} alternatives. They can anchor aggressively — "
                    "willing to take a bigger haircut on their BATNA because they have "
                    "multiple fallbacks. They should make the first offer to set the anchor. "
                    "They can credibly walk away."
                )
            elif num_alts == 1:
                anchoring = (
                    "User has exactly one alternative. Anchor firmly but don't take much "
                    "of a haircut on the BATNA — it's their only fallback. They should still "
                    "make the first offer if they've done their research. Don't bluff a walkaway "
                    "unless they're genuinely willing to take the alternative."
                )
            else:
                anchoring = (
                    "User has no concrete alternative. Use generic market analysis to set the "
                    "anchor — comparable deals, industry benchmarks, market rates. They should "
                    "still make the first offer based on research. Focus on value creation through "
                    "creative trades rather than hardball tactics. Never threaten to walk."
                )

            return json.dumps({
                "status": "recorded",
                "batna": self.batna,
                "anchoring_strategy": anchoring,
                "first_offer_advice": (
                    "Research shows it's generally better to make the first offer when you're "
                    "informed — it sets the anchor. Coach the user to go first if they've done "
                    "their homework on market rates and comparable deals."
                ),
            })

        elif tool_name == "add_issue":
            issue = {
                "name": tool_input["issue_name"],
                "options": tool_input["options"],
            }
            # Check for duplicates
            for existing in self.issues:
                if existing["name"].lower() == issue["name"].lower():
                    existing["options"] = issue["options"]
                    return json.dumps({
                        "status": "updated",
                        "issue": issue["name"],
                        "options": issue["options"],
                        "total_issues": len(self.issues),
                    })
            self.issues.append(issue)
            return json.dumps({
                "status": "added",
                "issue": issue["name"],
                "options": issue["options"],
                "total_issues": len(self.issues),
            })

        elif tool_name == "set_issue_range":
            issue_name = tool_input["issue_name"]
            worst = tool_input["worst_acceptable"]
            best = tool_input["best_hoped"]
            option_values = tool_input["option_values"]

            # Find the issue and attach range data
            found = False
            for issue in self.issues:
                if issue["name"].lower() == issue_name.lower():
                    # Compute 0-100 scores for each option based on range
                    range_span = best - worst
                    scores = {}
                    for opt_name, opt_val in option_values.items():
                        if range_span != 0:
                            scores[opt_name] = max(0, min(100, ((opt_val - worst) / range_span) * 100))
                        else:
                            scores[opt_name] = 50
                    issue["range"] = {
                        "worst": worst,
                        "best": best,
                        "option_values": option_values,
                        "scores": scores,
                    }
                    found = True
                    return json.dumps({
                        "status": "range_set",
                        "issue": issue["name"],
                        "scores": {k: round(v, 1) for k, v in scores.items()},
                        "note": "Scores now reflect where each option falls in the user's acceptable range.",
                    })

            if not found:
                return json.dumps({"error": f"Issue '{issue_name}' not found. Add it first with add_issue."})

        elif tool_name == "elicit_preference":
            # Store the pending elicitation — we'll process the user's answer
            self.pending_elicitation = {
                "scenario_a": tool_input["scenario_a"],
                "scenario_b": tool_input["scenario_b"],
                "issues_tested": tool_input["issues_tested"],
            }
            return json.dumps({
                "status": "question_prepared",
                "note": "Present the two scenarios naturally and ask which they'd prefer. Wait for their answer.",
            })

        elif tool_name == "analyze_deal":
            self.used_premium_tool = True
            case = self._build_case()
            if case is None:
                return json.dumps({"error": "No issues defined yet. Need to add terms first."})

            deal = tool_input["deal"]
            # Validate deal covers known issues
            missing = [i["name"] for i in self.issues if i["name"] not in deal]
            if missing:
                return json.dumps({
                    "error": f"Deal missing issues: {missing}",
                    "known_issues": [i["name"] for i in self.issues],
                })

            user_score, opponent_score = case.score_deal(deal)

            # Get frontier for context
            frontier = compute_pareto_frontier(case)
            max_joint = max(a + b for _, a, b in frontier) if frontier else 0

            # Find nearest frontier deal
            min_dist = float("inf")
            nearest = None
            better_for_user = None
            for f_deal, f_a, f_b in frontier:
                dist = ((user_score - f_a) ** 2 + (opponent_score - f_b) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest = f_deal
                if f_a > user_score and f_a + f_b >= user_score + opponent_score:
                    if better_for_user is None or f_a > better_for_user[1]:
                        better_for_user = (f_deal, f_a, f_b)

            joint = user_score + opponent_score
            value_pct = (joint / max_joint * 100) if max_joint > 0 else 0

            # Find which issues could be traded for improvement
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
                "user_satisfaction": f"{user_score / max(1, max(a for _, a, _ in frontier)) * 100:.0f}%",
                "joint_value_captured": f"{value_pct:.0f}%",
                "value_left_on_table": max_joint - joint,
                "distance_from_optimal": round(min_dist, 1),
                "deal_quality": (
                    "excellent" if min_dist < 3 else
                    "good" if min_dist < 10 else
                    "fair" if min_dist < 20 else
                    "poor — significant value left on the table"
                ),
                "suggested_trades": trade_suggestions,
                "better_deal_exists": better_for_user is not None,
                "better_deal": {k: v for k, v in better_for_user[0].items()} if better_for_user else None,
            })

        elif tool_name == "suggest_terms":
            existing = [t.lower() for t in tool_input.get("existing_issues", [])]
            neg_type = tool_input.get("negotiation_type", "general negotiation")

            # Use Claude to generate domain-appropriate term suggestions
            client = anthropic.Anthropic()
            suggestion_response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system="You are a negotiation expert. Respond ONLY with valid JSON, no other text.",
                messages=[{
                    "role": "user",
                    "content": f"""For a "{neg_type}" negotiation, suggest 5 additional terms/issues that are commonly negotiable but often overlooked.

Already being discussed: {json.dumps(tool_input.get("existing_issues", []))}

Respond with a JSON array of objects, each with:
- "term": the term name
- "why": why this term matters (1 sentence)
- "typical_options": array of 3-5 common options from worst to best for the person negotiating
- "tradeoff": what this term is commonly traded against (1 sentence)

Focus on terms that CREATE VALUE through trades — not obvious ones. The hidden terms are where the most value lives.""",
                }],
            )

            try:
                suggestions = json.loads(suggestion_response.content[0].text)
                # Filter out any that match existing issues
                suggestions = [
                    s for s in suggestions
                    if not any(s["term"].lower() in e or e in s["term"].lower() for e in existing)
                ][:5]
            except (json.JSONDecodeError, KeyError):
                suggestions = []

            return json.dumps({
                "negotiation_type": neg_type,
                "existing_issues": tool_input["existing_issues"],
                "missing_terms": suggestions,
                "instruction": (
                    "Surface these missing terms to the user. Frame each as a specific "
                    "question about their deal, not a generic suggestion. Explain WHY each "
                    "term matters and what the common tradeoff is. Focus on the ones most "
                    "likely to be relevant but unmentioned."
                ),
            })

        elif tool_name == "generate_counteroffers":
            self.used_premium_tool = True
            case = self._build_case()
            if case is None:
                return json.dumps({"error": "Need at least some issues defined first."})

            target_map = {"ambitious": 0.7, "moderate": 0.5, "conservative": 0.3}
            target = target_map.get(tool_input["target_satisfaction"], 0.5)

            # Use learned weights if available, otherwise use default
            weights = self.learned_weights if self.learned_weights else {
                issue["name"]: 1.0 / len(self.issues) for issue in self.issues
            }

            offers = generate_iso_utility_offers(
                case, weights, target_score=target, tolerance=0.2, max_offers=3,
            )

            if not offers:
                return json.dumps({
                    "error": "Could not generate counteroffers at this level. Try a different satisfaction level.",
                })

            self.last_offers = offers
            self.negotiation_round += 1

            formatted = []
            for i, offer in enumerate(offers):
                formatted.append({
                    "label": chr(65 + i),
                    "terms": offer,
                })

            return json.dumps({
                "counteroffers": formatted,
                "presentation_rule": (
                    "CRITICAL: The user must present ALL THREE offers to the counterpart "
                    "at the same time. NEVER suggest 'lead with A, fall back to B' — that "
                    "is negotiating against yourself, a spiraling point of weakness. "
                    "These offers are equally valuable to the user but differ across terms. "
                    "Whichever one the counterpart gravitates toward reveals THEIR priorities."
                ),
                "next_step": (
                    "Tell the user: 'Present all three packages to them. Come back to me "
                    "with their response — which one they lean toward, what they push back "
                    "on, and any counter they make. That reaction tells me exactly what "
                    "they care about, and I can build your next move from there.'"
                ),
            })

        elif tool_name == "process_counterpart_response":
            self.used_premium_tool = True
            case = self._build_case()
            if case is None:
                return json.dumps({"error": "No issues defined yet."})

            preferred = tool_input["preferred_package"].upper()
            pushback = tool_input.get("pushback_issues", [])
            counter = tool_input.get("counterpart_counter", {})

            # Infer counterpart weights from which package they preferred
            # The preferred package tells us which issues they value most
            preferred_idx = ord(preferred) - ord("A")
            if 0 <= preferred_idx < len(self.last_offers) and self.last_offers:
                preferred_offer = self.last_offers[preferred_idx]

                # Compare preferred offer to others — issues where the preferred
                # offer gives the counterpart MORE reveal their priorities
                weight_signal = {issue["name"]: 0.0 for issue in self.issues}
                for other_idx, other_offer in enumerate(self.last_offers):
                    if other_idx == preferred_idx:
                        continue
                    for issue in self.issues:
                        name = issue["name"]
                        if name in preferred_offer and name in other_offer:
                            pref_opt = preferred_offer[name]
                            other_opt = other_offer[name]
                            if pref_opt != other_opt:
                                # Counterpart preferred this option → they value this issue
                                opts = issue["options"]
                                if pref_opt in opts and other_opt in opts:
                                    # Higher index = better for user = worse for counterpart
                                    # If counterpart preferred lower index, they care about this issue
                                    pref_pos = opts.index(pref_opt)
                                    other_pos = opts.index(other_opt)
                                    if pref_pos < other_pos:
                                        weight_signal[name] += 1.0

                # Issues they pushed back on also signal high priority
                for issue_name in pushback:
                    if issue_name in weight_signal:
                        weight_signal[issue_name] += 1.5

                total = sum(weight_signal.values())
                if total > 0:
                    self.counterpart_weights = {k: v / total for k, v in weight_signal.items()}

            # Determine BATNA-weighted split for round 2
            batna_count = self.batna["count"] if self.batna else 0
            if batna_count >= 2:
                user_share = 0.75  # strong BATNA: take 75% of surplus
            elif batna_count == 1:
                user_share = 0.60  # moderate: take 60%
            else:
                user_share = 0.50  # no BATNA: even split

            # Compute frontier with both parties' weights
            user_weights = self.learned_weights if self.learned_weights else {
                issue["name"]: 1.0 / len(self.issues) for issue in self.issues
            }

            frontier = compute_pareto_frontier(case)
            if frontier:
                # Find the frontier point where user captures their BATNA-proportional share
                best_for_user = max(a for _, a, _ in frontier)
                worst_for_user = min(a for _, a, _ in frontier)
                target_user_score = worst_for_user + user_share * (best_for_user - worst_for_user)

                # Find closest frontier deal to target
                best_deal = None
                best_dist = float("inf")
                for deal, a_score, b_score in frontier:
                    dist = abs(a_score - target_user_score)
                    if dist < best_dist:
                        best_dist = dist
                        best_deal = deal
                        best_a = a_score
                        best_b = b_score

                return json.dumps({
                    "counterpart_priorities_inferred": self.counterpart_weights,
                    "batna_strength": f"{batna_count} alternatives",
                    "value_split": f"User gets {user_share:.0%} of surplus",
                    "round_2_target_deal": best_deal,
                    "round_2_user_score": best_a,
                    "round_2_counterpart_score": best_b,
                    "strategy": (
                        f"Based on their response, I now have a clearer picture of what they value. "
                        f"The round-2 offer moves toward the optimal frontier where both sides improve, "
                        f"but you capture {user_share:.0%} of the value-add based on your leverage. "
                        f"Both parties win compared to the current position — you just win more."
                    ),
                    "instruction": (
                        "Present this as a single refined offer. Explain why it works for both sides. "
                        "Frame it as: 'Based on your feedback, here's what I think works for both of us.'"
                    ),
                })
            else:
                return json.dumps({"error": "Need more issues to compute frontier."})

        elif tool_name == "get_coaching_insight":
            case = self._build_case()
            if case is None:
                return json.dumps({"insight": "Need to learn more about the negotiation first."})

            weights = self.learned_weights if self.learned_weights else {
                issue["name"]: 1.0 / len(self.issues) for issue in self.issues
            }

            # Find the max-joint-value frontier deal
            frontier = compute_pareto_frontier(case)
            if not frontier:
                return json.dumps({"insight": "Need more issues to analyze effectively."})

            best_joint = max(frontier, key=lambda x: x[1] + x[2])
            best_for_user = max(frontier, key=lambda x: x[1])

            sorted_weights = sorted(weights.items(), key=lambda x: -x[1])

            return json.dumps({
                "user_priorities": {k: f"{v:.0%}" for k, v in sorted_weights},
                "num_issues": len(self.issues),
                "num_elicitations_done": len(self.elicitation_choices),
                "frontier_size": len(frontier),
                "best_joint_deal": best_joint[0],
                "best_for_user_deal": best_for_user[0],
                "batna": self.batna,
                "advice": (
                    f"With {len(self.issues)} issues on the table, there are "
                    f"{len(frontier)} Pareto-optimal deals. "
                    + (f"We've done {len(self.elicitation_choices)} preference checks so far. "
                       f"More would improve accuracy. " if len(self.elicitation_choices) < 5 else "")
                    + "Focus trades on giving ground where you care least and pushing where you care most."
                ),
            })

        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def _process_elicitation_response(self, user_message: str):
        """If we have a pending elicitation, interpret the user's response."""
        if not self.pending_elicitation:
            return

        # Simple heuristic: if the user mentions "first" or "A" lean toward scenario_a
        msg_lower = user_message.lower()
        chose_a = any(w in msg_lower for w in ["first", "option a", "scenario a", "the first", "definitely a"])
        chose_b = any(w in msg_lower for w in ["second", "option b", "scenario b", "the second", "definitely b"])

        if not chose_a and not chose_b:
            # Use LLM to interpret
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=10,
                system="You determine which option a user chose. Respond with ONLY 'A' or 'B'.",
                messages=[{
                    "role": "user",
                    "content": f'Scenario A: {self.pending_elicitation["scenario_a"]}\n'
                               f'Scenario B: {self.pending_elicitation["scenario_b"]}\n'
                               f'User said: {user_message}\n'
                               f'Did they choose A or B?',
                }],
            )
            chose_a = "A" in response.content[0].text.upper()

        # Record the choice
        choice_data = {
            "elicitation": self.pending_elicitation,
            "chose": "a" if chose_a else "b",
        }
        self.elicitation_choices.append(choice_data)

        # Update weights based on accumulated choices
        self._update_weights_from_choices()
        self.pending_elicitation = None

    def _update_weights_from_choices(self):
        """Recompute weights from all elicitation choices so far."""
        if not self.elicitation_choices or not self.issues:
            return

        issue_names = [i["name"] for i in self.issues]
        n = len(issue_names)

        # Simple additive weight model:
        # When user chose scenario A over B, the issues where A was better
        # get weight credit. Accumulate across all choices.
        weight_scores = {name: 0.0 for name in issue_names}

        for choice_data in self.elicitation_choices:
            tested = choice_data["elicitation"]["issues_tested"]
            chosen = choice_data["chose"]

            # The first tested issue "wins" in scenario A, second in B
            # This is a simplification — the LLM constructs the scenarios
            # knowing which issues favor which scenario
            if len(tested) >= 2:
                if chosen == "a":
                    weight_scores[tested[0]] = weight_scores.get(tested[0], 0) + 1
                else:
                    weight_scores[tested[1]] = weight_scores.get(tested[1], 0) + 1

        total = sum(weight_scores.values())
        if total > 0:
            self.learned_weights = {k: v / total for k, v in weight_scores.items()}
        else:
            self.learned_weights = {name: 1.0 / n for name in issue_names}

    def chat(self, user_message: str) -> str:
        """Process a user message and return the coach's response."""
        # Check if we're awaiting an elicitation response
        if self.pending_elicitation:
            self._process_elicitation_response(user_message)

        self.messages.append({"role": "user", "content": user_message})
        self.chat_history.append({"role": "user", "content": user_message})

        # Call Claude with tools
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=self.messages,
        )

        # Process tool calls in a loop until we get a final text response
        while response.stop_reason == "tool_use":
            # Collect all tool uses and results
            assistant_content = response.content
            self.messages.append({"role": "assistant", "content": assistant_content})

            tool_results = []
            for block in assistant_content:
                if block.type == "tool_use":
                    result = self._handle_tool_call(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            self.messages.append({"role": "user", "content": tool_results})

            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=self.messages,
            )

        # Extract final text
        final_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_text += block.text

        self.messages.append({"role": "assistant", "content": response.content})
        self.chat_history.append({"role": "coach", "content": final_text})
        return final_text
