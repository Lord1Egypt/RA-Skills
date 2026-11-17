## Description:

Token Shark provides command-line style monitoring, token analysis, risk scoring, and price-alert workflows for newly listed crypto tokens.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[gztanht](https://clawhub.ai/user/gztanht)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to explore token-monitoring, token-analysis, risk-scoring, and price-alert command workflows. Its crypto outputs should be treated as demonstration output and not used for trading decisions without verified live data and independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token lists, audit status, liquidity-lock claims, risk scores, alerts, and position-size suggestions may be simulated or unverified and materially misleading for financial decisions.

Mitigation: Treat outputs as demonstration only; require verified live data sources, clear simulated-output labeling, and independent due diligence before any trading use.

Risk: Price alert commands may create local alert records.

Mitigation: Review command effects before running alert actions and remove local alert state when it is no longer needed.

Risk: The artifact includes crypto sponsorship addresses.

Mitigation: Do not send funds unless the recipient and purpose have been independently verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gztanht/skills/token-shark)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown and terminal-style text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price alert commands may create local alert state.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
