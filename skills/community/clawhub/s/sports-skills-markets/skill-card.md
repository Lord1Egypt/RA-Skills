## Description:

Markets connects ESPN live sports schedules with Kalshi and Polymarket prediction markets for unified dashboards, odds comparison, entity search, and bet evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonelli182](https://clawhub.ai/user/antonelli182)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare sports schedules, sportsbook odds, and prediction-market prices across ESPN, Kalshi, and Polymarket. It supports team or event search, market browsing, price normalization, arbitrage checks, and informational bet evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sportsbook odds, prediction-market prices, edge, arbitrage, and Kelly outputs can be stale, incomplete, or misleading if treated as financial advice.

Mitigation: Treat outputs as informational, verify live market data and calculations independently, and avoid using the skill to place trades automatically.

Risk: Kalshi, Polymarket, or ESPN data may be unavailable or only partially returned.

Mitigation: Review warnings in returned data, use available partial results cautiously, and retry or check the unavailable source directly before acting.

## Reference(s):

- [Markets API Reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/antonelli182/skills/sports-skills-markets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, tables, and JSON-shaped result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational and may include partial results when an external market data source is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
