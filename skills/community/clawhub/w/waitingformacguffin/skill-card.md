## Description:

Oscar prediction market intelligence from waitingformacguffin.com. Get live odds, whale activity, price movements, precursor awards, order book depth, and frontrunner changes across all 19 Oscar categories. Use when user asks about Oscar markets, betting odds, nominees, or wants a market update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonderspot](https://clawhub.ai/user/sonderspot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and summarize Oscar prediction-market data, including odds, whale activity, category movement, precursor effects, order book depth, and betting-style market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide betting-style Oscar market analysis that users may mistake for financial or gambling advice.

Mitigation: Treat outputs as informational, verify legality and eligibility in the user's jurisdiction, and avoid presenting analysis as financial advice.

Risk: The skill may call an external public API with curl.

Mitigation: Use only the documented public WaitingForMacGuffin endpoints and disclose that live external data may be fetched.

## Reference(s):

- [WaitingForMacGuffin](https://waitingformacguffin.com)
- [Oscar Brief API](https://waitingformacguffin.com/api/oscar/brief)
- [Oscar Research API](https://waitingformacguffin.com/api/oscar/research?query=Chalamet)
- [Oscar Precursor Simulation API](https://waitingformacguffin.com/api/oscar/simulate?precursor=dga&budget=500)
- [Precursor Data API](https://waitingformacguffin.com/api/precursors)
- [ClawHub Skill Page](https://clawhub.ai/sonderspot/skills/waitingformacguffin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional inline curl commands and API-derived market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include betting-style recommendations, risk tiers, portfolio simulations, and jurisdictional cautions.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
