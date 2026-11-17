## Description:

Gets TRC20 token lists on TRON with price, 24h change, 24h volume, market cap, holder count, and hot or trending token signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query TronScan MCP for TRON token lists, priced tokens, hot searches, and follow-up token details for market-data discovery and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token rankings, hot-search results, and quality-project sorting can be mistaken for investment recommendations.

Mitigation: Present the data as public market information and tell users to perform separate due diligence before relying on it.

Risk: An API key may be configured for higher TronScan API limits.

Mitigation: Store API keys only through the MCP configuration mechanism and avoid exposing them in prompts, logs, or skill files.

Risk: Some listed tokens may be flagged as hidden, suspicious, or unsafe by TronScan fields.

Mitigation: Flag tokens with tokenCanShow false or tokenLevel 3 or 4 as potentially risky before recommending further analysis.

## Reference(s):

- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)
- [ClawHub Skill Page](https://clawhub.ai/sshnii/skills/tronscan-token-list)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Guidance]

**Output Format:** [MCP tool calls with plain text or Markdown summaries of token-market data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include token price, 24h change, 24h volume, market cap, holder count, ranking, pagination, and risk-status fields.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
