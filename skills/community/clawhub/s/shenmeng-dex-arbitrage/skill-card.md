## Description:

Assists users with finding, monitoring, calculating, and planning DEX, cross-chain, triangular, flash-loan, and CEX-DEX arbitrage opportunities across chains such as Ethereum, BSC, and Arbitrum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate DEX arbitrage scenarios, estimate net profit after gas, slippage, protocol, and bridge costs, and draft monitoring or automation templates for arbitrage workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe billing code could expose users to billing risk.

Mitigation: Avoid running the billing code until reviewed; rotate the billing credential and load it from the declared environment variable.

Risk: Generated flash-loan contract templates could expose users to on-chain fund-loss risk if deployed as-is.

Mitigation: Add initiator checks, balance-delta accounting, nonzero slippage limits, safer signing guidance, and testnet or fork validation before any mainnet use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-dex-arbitrage)
- [搬砖套利基础](references/arbitrage-basics.md)
- [搬砖套利工具推荐](references/arbitrage-tools.md)
- [跨链桥指南](references/bridge-guide.md)
- [闪电贷套利](references/flashloan-arbitrage.md)
- [MEV防护指南](references/mev-protection.md)
- [Uniswap documentation](https://docs.uniswap.org/)
- [Flashbots documentation](https://docs.flashbots.net/)
- [1inch Developer Portal](https://portal.1inch.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with code blocks, Python and Solidity templates, calculations, and command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market-monitoring examples, profit calculations, and deployment guidance; financial and mainnet execution recommendations require independent review.]

## Skill Version(s):

2025.4.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
