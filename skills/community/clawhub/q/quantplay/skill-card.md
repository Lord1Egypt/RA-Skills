## Description:

Read a user's Indian broker accounts through Quantplay: positions, holdings, orders, margins, P&L history, option chains, expiries and live market data, across 10+ brokers (Zerodha, Upstox, Angel One, Kotak, Finvasia and more) from one connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantplay-admin](https://clawhub.ai/user/quantplay-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Indian broker accounts use this skill to review holdings, positions, open orders, margins, P&L, option chains, expiries and market prices across supported brokers. It provides read-only account analysis after the user signs in to Quantplay and approves access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive broker data, and the external service implementation was not audited.

Mitigation: Review Quantplay's OAuth permissions and existing account risk limits before connecting.

## Reference(s):

- [Quantplay skill on ClawHub](https://clawhub.ai/quantplay-admin/skills/quantplay)
- [Quantplay read-only MCP server](https://mcp.quantplay.tech/mcp/readonly)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Natural-language text, with tables when useful for account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account information; does not place, modify or cancel orders.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
