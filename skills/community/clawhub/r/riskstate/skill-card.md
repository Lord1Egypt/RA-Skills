## Description:

Pre-trade risk API for crypto trading agents. Returns exposure limits, allowed actions, and policy constraints for BTC/USD and ETH/USD from 30+ real-time signals. Spot, perpetual futures (perps), and DeFi borrowing aware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riskstate](https://clawhub.ai/user/riskstate)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, trading-agent builders, systematic trading teams, and capital desks use this skill to query RiskState before opening, sizing, or monitoring BTC/USD and ETH/USD spot, perpetual futures, or DeFi borrowing positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence automated crypto-trading decisions.

Mitigation: Treat outputs as third-party risk inputs, require human review or independent exposure limits for material trades, and do not execute solely from the policy response.

Risk: Optional DeFi checks may send wallet addresses to a third-party API.

Mitigation: Avoid operational wallet addresses unless DeFi-specific checks are necessary, and confirm the publisher's wallet-data logging and retention practices.

Risk: The artifact documents an unpinned MCP server install path.

Mitigation: Pin package or container versions and run the MCP server in a sandbox before connecting it to trading workflows.

Risk: The API documentation discloses a known scoring divergence affecting whale and tactical-volume readings until a corrected scoring version is deployed.

Mitigation: Use human review or independent limits for material trades until the corrected scoring version is released and verified.

Risk: Stale, degraded, or low-confidence market data can reduce policy reliability.

Mitigation: Follow the artifact's failure guidance: downgrade conviction, halve or avoid position sizing when data quality is degraded, and fail closed on timeouts or core data errors.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/riskstate/skills/riskstate)
- [RiskState website](https://riskstate.ai)
- [RiskState API documentation](https://riskstate.ai/docs/api)
- [Local API reference](docs/api-v1.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bearer-token authentication through RISKSTATE_API_KEY and returns risk-policy fields from a third-party API.]

## Skill Version(s):

1.4.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
