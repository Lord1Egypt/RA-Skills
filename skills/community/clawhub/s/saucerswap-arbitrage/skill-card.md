## Description:

Perform triangular arbitrage on Hedera using SaucerSwap to find, calculate, and execute profitable multi-hop token swaps atomically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harleyscodes](https://clawhub.ai/user/harleyscodes)

### License/Terms of Use:


## Use Case:

Developers and DeFi operators use this skill to identify SaucerSwap triangular arbitrage routes on Hedera, calculate potential profit across pools, and prepare multi-hop swap execution guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides unsafe and incomplete mainnet trading instructions that could cause financial loss if followed directly.

Mitigation: Do not allow an agent to trade real funds without explicit confirmation, testnet or dry-run defaults, full route validation, quote freshness checks, fee and slippage accounting, and transaction parameters that enforce minimum output and deadlines.

## Reference(s):

- [SaucerSwap route API endpoint](https://mainnet-api.saucerswap.fi/route?from=${tokenA}&to=${tokenB}&amount=${amountIn})

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mainnet contract addresses, token identifiers, quote-fetching snippets, arbitrage path examples, and safety-check guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
