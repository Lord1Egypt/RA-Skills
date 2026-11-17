## Description:

Analyzes public TRON accounts for asset holdings, token balances, staking and voting activity, resource usage, transaction patterns, and DeFi participation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greason](https://clawhub.ai/user/greason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to query TronGrid and summarize public TRON wallet balances, token holdings, staking and voting behavior, resource usage, transaction history, and DeFi participation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet profiling can expose sensitive behavioral patterns even when the underlying TRON data is public.

Mitigation: Use the skill only for intended wallet analysis, request narrow balance-only checks when appropriate, and treat aggregated profiles as sensitive.

## Reference(s):

- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)
- [ClawHub skill page](https://clawhub.ai/greason/skills/trongrid-account-profiling)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown account profile with tables and concise analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only TronGrid API call guidance and partial results when some API calls fail.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
