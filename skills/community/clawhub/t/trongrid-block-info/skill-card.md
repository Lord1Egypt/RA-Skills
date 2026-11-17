## Description:

Query and analyze TRON blocks, including producer info, transaction breakdown, rewards, burns, network load, single block lookup, block ranges, confirmed blocks, and multi-block trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greason](https://clawhub.ai/user/greason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to answer TRON block questions with structured reports on block headers, producers, transactions, fees, burns, rewards, and recent network load trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent makes TronGrid MCP queries for public blockchain data.

Mitigation: Install and use the skill only when those external read-only queries are acceptable for the intended environment.

Risk: Reward, burn, and fee calculations are analytical output and may become stale or incorrect if TRON network parameters change.

Mitigation: Verify live network parameters and source data before using results for decisions involving money.

## Reference(s):

- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)
- [ClawHub Skill Page](https://clawhub.ai/greason/skills/trongrid-block-info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown reports with tables and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only TronGrid MCP queries for public blockchain data; analytical calculations should be verified for financial decisions.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
