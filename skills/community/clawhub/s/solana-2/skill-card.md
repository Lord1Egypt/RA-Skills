## Description:

Query Solana blockchain data with USD pricing, including wallet balances, token portfolios, transaction details, NFTs, whale detection, network stats, and token prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agungprabowo123](https://clawhub.ai/user/agungprabowo123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Solana wallet, token, transaction, NFT, whale-transfer, network, and price data through read-only RPC and CoinGecko lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, transaction signatures, and token mints are sent to Solana RPC providers and CoinGecko for lookups.

Mitigation: Use the default endpoint or a trusted HTTPS RPC endpoint, and avoid sending sensitive lookup patterns to RPC providers you do not trust.

Risk: An untrusted SOLANA_RPC_URL endpoint can return inaccurate blockchain data or expose query activity.

Mitigation: Set SOLANA_RPC_URL only to a trusted provider and review results before relying on them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agungprabowo123/skills/solana-2)
- [Publisher profile](https://clawhub.ai/user/agungprabowo123)
- [Default Solana RPC endpoint](https://api.mainnet-beta.solana.com)
- [CoinGecko Solana price API endpoint](https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; helper script returns JSON-formatted blockchain and price lookup results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only network lookups; output may vary with RPC availability, CoinGecko rate limits, and current chain state.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
