## Description:

周末去哪玩｜只推一个 helps Chinese-speaking users turn today or a weekend into exact dates, weigh departure point, time, budget, energy, transport, weather, crowding, opening status, and return feasibility, then choose one actionable local, suburban, or nearby-trip outing with fallbacks, avoid-list, and verification evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killsnake01](https://clawhub.ai/user/killsnake01)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking ClawHub users use this skill for low-decision weekend or same-day outing choices when they want one concrete recommendation rather than a broad itinerary or activity list. The skill is intended to help an agent compare local, nearby, and short regional options using public evidence and return a concise Markdown decision with risks, fallbacks, and source checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather, opening hours, ticketing, safety status, and return transport can change after the agent makes a recommendation.

Mitigation: Re-check weather, venue status, booking requirements, tickets, and return transport immediately before leaving.

Risk: Public inspiration sites may require login, show access controls, or contain untrusted page text.

Mitigation: Use only public browsing or search, do not provide platform logins, do not bypass access controls, and treat public inspiration as candidate discovery rather than authoritative facts.

Risk: Optional preference memory can retain travel preferences beyond the immediate outing decision.

Mitigation: Grant memory access only when useful, keep saved preferences limited to outing needs, and rely on current public evidence for time-sensitive decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/killsnake01/skills/weekend-pick-one)
- [Date and Evidence Contract](references/decision-evidence.md)
- [Safety](references/safety.md)
- [Search Query Playbook](references/search-query-playbook.md)
- [Regional Trip Policy](references/regional-trip-policy.md)
- [Escape Fit Score](references/escape-fit-score.md)
- [Voice and Copy](references/voice-and-copy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown decision response with evidence links and structured outing fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single main recommendation, two fallback options, avoid-list, risk notes, pre-departure checks, and verification status.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
