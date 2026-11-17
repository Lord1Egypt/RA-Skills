## Description:

Query crypto wallet portfolios, transactions, DeFi positions, NFTs, token prices, and gas fees across EVM chains and Solana using Zerion's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abishekdharshan](https://clawhub.ai/user/abishekdharshan)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agent users use this skill to query Zerion wallet and market data for portfolio analysis, transaction review, DeFi position research, NFT holdings, token prices, and gas fees across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet queries sent to the remote Zerion MCP server may include customer, internal, or investigatory wallet data.

Mitigation: Use only authorized wallet data and confirm the provider's data-handling terms before sending sensitive or regulated queries.

Risk: Installing from an unverified command or elevated shell can increase local installation risk.

Mitigation: Prefer a pinned or verified ClawHub installer when available and install from a normal user shell.

Risk: The required Zerion API key can expose account access if copied into shared files or transcripts.

Mitigation: Store the API key only in the MCP client's local secret or configuration mechanism and rotate it if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abishekdharshan/skills/zerion-api-mcp)
- [Zerion API documentation](https://developers.zerion.io)
- [Building with AI](https://developers.zerion.io/reference/building-with-ai)
- [Zerion llms.txt](https://developers.zerion.io/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown or plain text responses with MCP configuration examples when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Zerion API key and sends authorized wallet-data queries to Zerion's remote MCP server.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
