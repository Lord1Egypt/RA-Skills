"""Strategic negotiation agent that uses iso-utility offers to learn
the counterpart's weights and push toward the Pareto frontier.

The strategy:
1. Early rounds: Present iso-utility offer SETS (same score for us,
   varied across issues) to probe the counterpart's preferences.
2. Infer counterpart weights from which offers they gravitate toward.
3. Later rounds: Use both parties' weights to identify Pareto-optimal
   deals and propose them.
"""
from __future__ import annotations

import json
from typing import Optional

import anthropic

from case import NegotiationCase
from elicitation import (
    compute_weighted_score,
    generate_iso_utility_offers,
)
from scorer import compute_weighted_pareto_frontier


def _build_weight_map(case: NegotiationCase, party: str) -> dict[str, float]:
    """Convert fixed case scores into normalized weights for a party."""
    issues = case.issues
    # Sum up total points available per issue, use as proxy for importance
    totals = {}
    for issue in issues:
        scores = issue.party_a_scores if party == "a" else issue.party_b_scores
        # Weight = range of scores for this issue (max - min)
        vals = list(scores.values())
        totals[issue.name] = max(vals) - min(vals)

    total_range = sum(totals.values())
    if total_range == 0:
        return {name: 1.0 / len(issues) for name in totals}
    return {name: val / total_range for name, val in totals.items()}


def _infer_counterpart_weights(
    case: NegotiationCase,
    our_offers: list[list[dict[str, str]]],
    their_responses: list[str],
) -> dict[str, float]:
    """Infer the counterpart's weights from their responses to our offer sets.

    Uses an LLM to parse which of our offers they gravitated toward,
    then derives weights from the pattern.
    """
    if not our_offers or not their_responses:
        # No data yet — assume uniform
        return {issue.name: 1.0 / len(case.issues) for issue in case.issues}

    client = anthropic.Anthropic()

    issues_desc = []
    for issue in case.issues:
        opts = ", ".join(f'"{o}"' for o in issue.options)
        issues_desc.append(f"- {issue.name}: {opts}")
    issues_block = "\n".join(issues_desc)

    offer_history = []
    for round_idx, (offers, response) in enumerate(zip(our_offers, their_responses)):
        offer_lines = []
        for i, offer in enumerate(offers):
            terms = ", ".join(f"{k}: {v}" for k, v in offer.items())
            offer_lines.append(f"  Option {chr(65+i)}: {terms}")
        offer_history.append(
            f"Round {round_idx+1} — We presented:\n"
            + "\n".join(offer_lines)
            + f"\n\nTheir response:\n{response}"
        )

    history_block = "\n\n---\n\n".join(offer_history)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="You analyze negotiation responses to infer preferences. Respond ONLY in the exact JSON format requested.",
        messages=[{
            "role": "user",
            "content": f"""Analyze this negotiation counterpart's responses to infer their relative preferences.

ISSUES:
{issues_block}

OFFER/RESPONSE HISTORY:
{history_block}

Based on which offers they gravitated toward and what they emphasized in their responses,
estimate their relative weight for each issue (how important each issue is to them).

Respond with ONLY a JSON object mapping issue names to weights (0.0 to 1.0, summing to 1.0):
{{"issue_name": weight, ...}}""",
        }],
    )

    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    try:
        raw_weights = json.loads(text)
        # Normalize
        total = sum(raw_weights.values())
        if total > 0:
            return {k: v / total for k, v in raw_weights.items()}
    except (json.JSONDecodeError, AttributeError):
        pass

    # Fallback: uniform
    return {issue.name: 1.0 / len(case.issues) for issue in case.issues}


class SmartNegotiationAgent:
    """A strategic agent that uses iso-utility offers to learn counterpart weights."""

    def __init__(
        self,
        case: NegotiationCase,
        party: str,
        model: str = "claude-sonnet-4-6",
    ):
        self.case = case
        self.party = party
        self.model = model
        self.name = case.party_a_name if party == "a" else case.party_b_name
        self.opponent_name = case.party_b_name if party == "a" else case.party_a_name
        self.own_weights = _build_weight_map(case, party)
        self.inferred_opponent_weights = {
            issue.name: 1.0 / len(case.issues) for issue in case.issues
        }
        self.messages: list[dict] = []
        self.client = anthropic.Anthropic()
        self.offers_presented: list[list[dict[str, str]]] = []
        self.opponent_responses: list[str] = []
        self.round_num = 0

        # Build system prompt
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        if self.party == "a":
            role = self.case.party_a_role
            background = self.case.party_a_background
            batna = self.case.party_a_batna_score
            scoring_lines = []
            for issue in self.case.issues:
                opts = ", ".join(
                    f'"{opt}" = {pts} pts' for opt, pts in issue.party_a_scores.items()
                )
                scoring_lines.append(f"  - {issue.name}: {opts}")
        else:
            role = self.case.party_b_role
            background = self.case.party_b_background
            batna = self.case.party_b_batna_score
            scoring_lines = []
            for issue in self.case.issues:
                opts = ", ".join(
                    f'"{opt}" = {pts} pts' for opt, pts in issue.party_b_scores.items()
                )
                scoring_lines.append(f"  - {issue.name}: {opts}")

        scoring_block = "\n".join(scoring_lines)
        issue_names = ", ".join(issue.name for issue in self.case.issues)

        is_vc = "term sheet" in self.case.title.lower() or "vc" in self.case.title.lower()
        vc_context = ""
        if is_vc:
            if self.party == "a":
                vc_context = """
VC CONTEXT — You are a founder. Frame your 3 packages as different deal structures:
- One that emphasizes clean economics (non-participating, lower valuation)
- One that trades structure for headline valuation
- One that optimizes for control (board seats, limited provisions)
Use founder language: "Here are three structures we could work with" not "here are three options."
Reference real tradeoffs: "We'd take a lower headline if the structure is cleaner."
"""
            else:
                vc_context = """
VC CONTEXT — You are an investor. Frame your 3 packages as different investment structures:
- One that emphasizes downside protection (participating preferred, board control)
- One that trades governance for better economics (higher ownership)
- One that balances both with moderate terms
Use investor language: "Here are three structures our partnership could support."
Reference fund obligations: "Our LPs expect certain governance protections at this check size."
"""

        return f"""You are {self.name}, {role}.

SCENARIO: {self.case.title}
{self.case.description}

You are negotiating with {self.opponent_name}. Issues: {issue_names}.

BACKGROUND (private):
{background}

YOUR PRIVATE SCORING:
{scoring_block}

BATNA (no-deal score): {batna} points.
{vc_context}
NEGOTIATION STRATEGY:
You are a strategic negotiator. Your approach:

1. PRESENT OFFER SETS: When making proposals, present exactly 3 deal packages
   rather than a single proposal. Frame them as different structures you could
   work with. These 3 packages should be approximately equal in value to YOU
   but vary across issues. This lets you learn what THEY value.

2. OBSERVE REACTIONS: Pay close attention to which package the counterpart
   gravitates toward. Their preference reveals their priorities.

3. TRADE STRATEGICALLY: Once you understand their priorities, propose trades
   that give them what they value most (cheap for you) in exchange for what
   YOU value most (cheap for them). This creates joint value.

4. CLOSE EFFICIENTLY: Push toward deals that maximize joint value — where
   neither side can do better without the other doing worse.

RULES:
- Negotiate naturally in first person as {self.name}.
- NEVER reveal your exact point values.
- Always present proposals as sets of 3 packages when possible.
- Keep responses concise (2-4 paragraphs max).
- Use realistic deal language, not generic negotiation phrases.
- When agreement is reached, end with:
  DEAL AGREED: [list each issue and its agreed option]

IMPORTANT: When told to present specific offers, weave them naturally into
your negotiation. Don't say "here are three equal-value options" — frame them
as different deal structures you could support.
"""

    def _get_iso_offers(self, target: float = 0.5) -> list[dict[str, str]]:
        """Generate iso-utility offers at the current target level."""
        offers = generate_iso_utility_offers(
            self.case,
            self.own_weights,
            target_score=target,
            tolerance=0.15,
            max_offers=3,
        )
        if len(offers) < 3:
            # Widen tolerance
            offers = generate_iso_utility_offers(
                self.case,
                self.own_weights,
                target_score=target,
                tolerance=0.25,
                max_offers=3,
            )
        return offers

    def _get_frontier_offer(self) -> dict[str, str] | None:
        """Find a Pareto-optimal deal that balances both parties' inferred preferences."""
        frontier = compute_weighted_pareto_frontier(
            self.case, self.own_weights, self.inferred_opponent_weights
        )
        if not frontier:
            return None

        # Pick the frontier deal with highest joint score
        best = max(frontier, key=lambda x: x[1] + x[2])
        return best[0]

    def respond(self, opponent_message: str | None = None) -> str:
        """Generate a strategic response."""
        self.round_num += 1

        if opponent_message is not None:
            self.opponent_responses.append(opponent_message)
            self.messages.append({"role": "user", "content": opponent_message})

            # Update inferred weights after round 2+
            if len(self.opponent_responses) >= 2:
                self.inferred_opponent_weights = _infer_counterpart_weights(
                    self.case, self.offers_presented, self.opponent_responses
                )

        # Decide strategy based on round
        if self.round_num <= 2:
            # Exploration phase: present iso-utility offer sets
            target = 0.6 if self.round_num == 1 else 0.5
            offers = self._get_iso_offers(target)
            if offers:
                self.offers_presented.append(offers)
                offer_text = self._format_offers_for_prompt(offers)
                instruction = (
                    f"Present these three deal packages naturally as options you could work with. "
                    f"Frame them as different approaches, not as equal-value offers:\n{offer_text}"
                )
            else:
                instruction = "Make your opening proposal."

            if opponent_message is None:
                self.messages.append({
                    "role": "user",
                    "content": f"The negotiation is starting. {instruction}",
                })
            else:
                self.messages.append({
                    "role": "user",
                    "content": instruction,
                })
                self.messages[-2] = {"role": "user", "content": opponent_message}
                # Restructure: opponent message then instruction as system guidance
                # Actually, let's use a simpler approach
                self.messages = self.messages[:-2]
                self.messages.append({
                    "role": "user",
                    "content": f"{opponent_message}\n\n[STRATEGIC NOTE - not part of conversation: {instruction}]",
                })
        else:
            # Convergence phase: use inferred weights to find frontier deals
            frontier_deal = self._get_frontier_offer()
            if frontier_deal:
                deal_text = ", ".join(f"{k}: {v}" for k, v in frontier_deal.items())
                weights_text = ", ".join(
                    f"{k}: {v:.0%}" for k, v in
                    sorted(self.inferred_opponent_weights.items(), key=lambda x: -x[1])
                )
                instruction = (
                    f"[STRATEGIC NOTE: Based on their responses, their estimated priorities are: "
                    f"{weights_text}. A Pareto-optimal deal would be: {deal_text}. "
                    f"Push toward this deal. If close to agreement, finalize it.]"
                )
                self.messages[-1] = {
                    "role": "user",
                    "content": f"{opponent_message}\n\n{instruction}",
                }

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.messages,
        )

        reply = response.content[0].text
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def _format_offers_for_prompt(self, offers: list[dict[str, str]]) -> str:
        lines = []
        for i, offer in enumerate(offers):
            terms = ", ".join(f"{k}: {v}" for k, v in offer.items())
            lines.append(f"  Package {chr(65+i)}: {terms}")
        return "\n".join(lines)
