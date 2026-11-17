## Description:

Explore Web3 on-chain data using Chainbase APIs for blockchain data, token holders, wallet addresses, token prices, NFTs, ENS domains, transactions, DeFi portfolios, and other on-chain analytics across EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxcong](https://clawhub.ai/user/lxcong)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agent users use this skill to route natural-language Web3 questions to Chainbase API calls or SQL queries and present on-chain results such as holders, balances, transfers, NFT data, ENS records, and wallet analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web3 identifiers, custom SQL queries, and the configured Chainbase API key are sent to Chainbase.

Mitigation: Avoid submitting proprietary watchlists or sensitive address-query combinations unless sharing them with Chainbase is intended.

Risk: The skill performs expected external network calls to Chainbase APIs.

Mitigation: Review the generated API request or SQL query before execution and configure CHAINBASE_API_KEY only in trusted environments.

## Reference(s):

- [Chainbase API Endpoint Reference](references/api-endpoints.md)
- [Chainbase](https://chainbase.com)
- [Chainbase Console](https://console.chainbase.com)
- [ClawHub skill page](https://clawhub.ai/lxcong/skills/web3-data)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, tables, and JSON API results when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chainbase Web3 API requests, SQL API queries, and summarized on-chain results.]

## Skill Version(s):

1.0.0 (source: release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
