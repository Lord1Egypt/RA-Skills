"""LLM-powered negotiation agent using Claude API."""
from __future__ import annotations

import anthropic

from case import NegotiationCase


def _build_system_prompt(case: NegotiationCase, party: str) -> str:
    """Build a system prompt for a negotiation agent."""
    if party == "a":
        name = case.party_a_name
        role = case.party_a_role
        background = case.party_a_background
        batna_score = case.party_a_batna_score
        opponent_name = case.party_b_name
        scoring_lines = []
        for issue in case.issues:
            opts = ", ".join(
                f'"{opt}" = {pts} pts' for opt, pts in issue.party_a_scores.items()
            )
            scoring_lines.append(f"  - {issue.name}: {opts}")
    else:
        name = case.party_b_name
        role = case.party_b_role
        background = case.party_b_background
        batna_score = case.party_b_batna_score
        opponent_name = case.party_a_name
        scoring_lines = []
        for issue in case.issues:
            opts = ", ".join(
                f'"{opt}" = {pts} pts' for opt, pts in issue.party_b_scores.items()
            )
            scoring_lines.append(f"  - {issue.name}: {opts}")

    scoring_block = "\n".join(scoring_lines)
    issue_names = ", ".join(issue.name for issue in case.issues)

    # Determine if this is a VC negotiation for role-specific language
    is_vc = "term sheet" in case.title.lower() or "vc" in case.title.lower()

    if is_vc:
        role_guidance = _vc_role_guidance(party, name)
    else:
        role_guidance = ""

    return f"""You are {name}, {role}.

SCENARIO: {case.title}
{case.description}

You are negotiating with {opponent_name}. The issues on the table are: {issue_names}.

BACKGROUND (private — do not reveal):
{background}

YOUR PRIVATE SCORING (do not reveal exact point values):
{scoring_block}

If you walk away with no deal, you get {batna_score} points (your BATNA).
{role_guidance}
NEGOTIATION RULES:
- Negotiate naturally in first person as {name}.
- You may discuss priorities in general terms but NEVER reveal your exact point values.
- Make proposals, counterproposals, and trade-offs across issues.
- Try to maximize YOUR score while finding a mutually acceptable deal.
- When you reach an agreement, state it clearly with all issue resolutions.
- Keep responses concise (2-4 paragraphs max).
- Use realistic deal language. Avoid generic negotiation phrases.
- When you and your counterpart agree on all issues, end your message with exactly:
  DEAL AGREED: [list each issue and its agreed option]
"""


def _vc_role_guidance(party: str, name: str) -> str:
    """Return VC-specific behavioral guidance based on role."""
    if party == "a":
        # Founder
        return """
VC FOUNDER BEHAVIOR — negotiate like a real founder:
- Prioritize valuation and control. Resist heavy preferences.
- Trade structure for headline valuation when it makes sense.
- Care about signaling and future round dynamics.
- Reference competing interest or term sheets when you have leverage.
- Push back on vesting resets — you've been building for years.
- Use language like: "We'd want clean terms at that price" or "That liquidation structure is aggressive for this stage."
- Think about downstream effects: "A participating preferred sets a bad precedent for our Series B."
"""
    else:
        # VC / Investor
        return """
VC INVESTOR BEHAVIOR — negotiate like a real GP:
- Push on downside protection (preferences, control provisions).
- Trade valuation for structure — you'd rather pay more for better terms.
- Anchor around ownership targets (15-20% for Series A).
- Insist on governance rights proportional to your check size.
- Use language like: "We're fine at this valuation, but we'd want a 1x participating preference and a board seat."
- Reference LP obligations: "Our fund docs require certain governance protections."
- Think about portfolio construction: "We need pro-rata to maintain our position in future rounds."
"""


class NegotiationAgent:
    """An LLM-powered negotiation agent."""

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
        self.system_prompt = _build_system_prompt(case, party)
        self.messages: list[dict] = []
        self.client = anthropic.Anthropic()

    def respond(self, opponent_message: str | None = None) -> str:
        """Generate a response, optionally given the opponent's last message."""
        if opponent_message is not None:
            self.messages.append({"role": "user", "content": opponent_message})
        elif not self.messages:
            # First move — prompt to open
            self.messages.append({
                "role": "user",
                "content": "The negotiation is starting. Please make your opening statement and initial proposal.",
            })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.messages,
        )

        reply = response.content[0].text
        self.messages.append({"role": "assistant", "content": reply})
        return reply
