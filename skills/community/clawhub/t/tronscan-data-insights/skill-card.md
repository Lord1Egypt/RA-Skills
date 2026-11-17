## Description:

TRON network insights for new accounts, daily transaction count, transaction type distribution, hot tokens, hot contracts, top accounts by transaction count, and staked TRX rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to retrieve and interpret aggregate TRON network activity, token, contract, account-ranking, resource, and DeFi TVL metrics through TronScan MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Address-level cross-chain lookup may route a single TRON address to TronScan despite the skill's non-profiling scope.

Mitigation: Use aggregate analytics tools by default and invoke cross-chain address lookup only when the user explicitly requests that lookup and accepts sending the address to TronScan.

Risk: TronScan API rate limits or narrow time-range defaults may produce incomplete or empty analytics results.

Mitigation: Check requested date ranges and retry with configured TronScan API access when rate limits or 429 errors occur.

## Reference(s):

- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)
- [ClawHub skill page](https://clawhub.ai/sshnii/skills/tronscan-data-insights)
- [Publisher profile](https://clawhub.ai/user/sshnii)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text summaries with TronScan MCP tool call guidance and returned analytics data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time ranges, ranking categories, token or contract dimensions, and TronScan result fields depending on the requested metric.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
