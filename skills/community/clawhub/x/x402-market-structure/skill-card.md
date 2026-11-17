## Description:

Real-time crypto market intelligence for live exchange orderflow, directional regime detection, historical OHLCV with buy/sell flow, and on-chain address risk profiling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tunedforai](https://clawhub.ai/user/tunedforai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading agents use this skill to query live crypto market structure, macro regime signals, historical bars, and wallet-address risk through native MCP tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market queries and wallet addresses are sent to x402.tunedfor.ai and may be linkable to the user's interests or identity by the service operator.

Mitigation: Use only queries and wallet addresses appropriate to share with that service, and avoid sensitive or unnecessary address lookups.

Risk: Wallet secrets, exchange credentials, or seed phrases could expose funds if provided during use.

Mitigation: Do not provide seed phrases, private keys, exchange credentials, or other wallet secrets to the skill or remote service.

Risk: Live market outputs can become stale or be constrained by free-tier rate limits.

Mitigation: Check freshness indicators such as stale status before relying on returned data, and independently review market signals before taking action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tunedforai/skills/x402-market-structure)
- [Publisher Profile](https://clawhub.ai/user/tunedforai)
- [x402 MCP Endpoint](https://x402.tunedfor.ai/mcp)
- [x402 REST API Base](https://x402.tunedfor.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool calls and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a remote MCP service; MCP tools are free and rate-limited, with no API key or wallet required.]

## Skill Version(s):

1.2.0 (source: artifact frontmatter, evidence release, and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
