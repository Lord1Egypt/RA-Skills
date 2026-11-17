## Description:

Query TRON wallet addresses for total assets, token holdings, DeFi participation, energy and bandwidth, votes, transfer counts, and related account activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to profile TRON wallet addresses, inspect balances and token holdings, review staking resources, evaluate approvals, and summarize account activity through the TronScan MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet profiling can expose privacy-sensitive public blockchain activity and related-account patterns.

Mitigation: Use the skill only for addresses the user is authorized or comfortable analyzing, and explain that public blockchain signals can be sensitive.

Risk: Risk tags, approval data, related accounts, and activity patterns may be misleading without additional context.

Mitigation: Present these outputs as analysis signals rather than definitive conclusions, and encourage review against the underlying TronScan results.

Risk: Queries are sent to the configured TronScan MCP service.

Mitigation: Install and use the skill only when sending TRON addresses and related questions to that service is acceptable.

## Reference(s):

- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)
- [ClawHub Skill Page](https://clawhub.ai/sshnii/skills/tronscan-account-profiler)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance]

**Output Format:** [Markdown or text summaries with referenced TronScan MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet balances, token holdings, DeFi participation, staking resources, approvals, tags, and activity summaries.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
