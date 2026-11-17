## Description:

Query blockchain wallet data, token prices, and transaction history using the Zerion API via its MCP connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vshamanov](https://clawhub.ai/user/vshamanov)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to query Zerion wallet, token, NFT, DeFi position, PnL, transaction, and price-chart data for web3 portfolio analysis and related dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Zerion API keys may be exposed when they are pasted into chat or sent inside model prompt text from generated dashboards.

Mitigation: Use a dedicated secret/auth channel or direct Zerion Authorization headers, and do not place API keys in prompts, logs, files, or rendered artifacts.

Risk: Wallet and token queries can reveal sensitive portfolio, transaction, and holdings data.

Mitigation: Disclose wallet-data privacy implications and limit queries and sharing to addresses and data the user intends to analyze.

## Reference(s):

- [Wallet Endpoints Reference](references/wallet-endpoints.md)
- [Fungible & NFT Endpoints Reference](references/fungible-nft-endpoints.md)
- [Zerion MCP Server](https://developers.zerion.io/mcp)
- [Zerion Developer Dashboard](https://dashboard.zerion.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint references, code examples, and JSON response-shape examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Zerion API key for authenticated requests; responses may include wallet, token, NFT, DeFi, PnL, transaction, and price data.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
