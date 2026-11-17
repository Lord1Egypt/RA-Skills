## Description:

Provide TRON network analytics including transaction volume, type distribution, hot contracts, trending tokens, active accounts, staking metrics, and resource economics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greason](https://clawhub.ai/user/greason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to query TronGrid MCP data and compile TRON network health, activity, contract, token, account, governance, staking, and resource-economics reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blockchain and market figures can be stale, incomplete, or misleading if sampled from a short block window or external market-data sources.

Mitigation: Verify financial figures from authoritative sources and state the sampled block range and any missing data in generated reports.

Risk: Using the skill requires configuring the TronGrid MCP server and allowing the agent to query public blockchain and market-data sources.

Mitigation: Confirm the MCP server configuration and approved data sources before installation or use.

## Reference(s):

- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown analytics report with tables and concise findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only public blockchain analytics queries and may include current market context when requested.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
