## Description:

Browse and rank TRC-20 and TRC-10 tokens on TRON using TronGrid-backed token metadata, holder counts, recent activity, supply, and category filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greason](https://clawhub.ai/user/greason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer TRON token discovery questions, profile known TRC-20 contracts, inspect TRC-10 assets, and summarize on-chain token signals from TronGrid. It is best suited for token metadata, holder, supply, contract, and recent activity summaries rather than financial market rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill description advertises price, volume, and market-cap rankings that TronGrid cannot provide on its own.

Mitigation: Use the skill for on-chain token metadata, holder, supply, contract, and activity summaries; require a separate trusted market-data source for price, trading volume, market capitalization, or investment analysis.

## Reference(s):

- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)
- [ClawHub skill page](https://clawhub.ai/greason/skills/trongrid-token-list)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and tables with concise notes about data availability]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TronGrid tool names, token contract addresses, on-chain activity signals, and caution notes when requested market data is unavailable.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
