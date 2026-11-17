## Description:

Starknet L2 DeFi integration toolkit for AI agents that reads balances, fetches STRK and ETH quotes, lists Ekubo and JediSwap pools, simulates swaps, and produces Cairo contract skeletons using public Starknet JSON-RPC endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and simulate Starknet DeFi activity, including token balances, public price quotes, liquidity pool data, swap estimates, and starter Cairo contract scaffolds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold command can create or overwrite Cairo files based on unchecked input.

Mitigation: Run scaffold only in a clean project directory, use simple identifier-like names and symbols, and inspect the output path before keeping generated files.

Risk: Generated Cairo contract skeletons are unaudited starter code.

Mitigation: Review, test, and audit generated Cairo before compiling, deploying, or connecting it to assets.

Risk: Public RPC and API endpoints may be rate-limited or unavailable.

Mitigation: Use a production Starknet RPC endpoint through STARKNET_RPC_URL and handle transient API failures in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/starknet-defi-toolkit)
- [Starknet Lava RPC endpoint](https://rpc.starknet.lava.build)
- [Starknet Sepolia Lava RPC endpoint](https://rpc.starknet-testnet.lava.build)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids={cg_id}&vs_currencies=usd)
- [Ekubo pools API](https://mainnet-api.ekubo.org/pools)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands, plaintext command output, and generated Cairo code files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only RPC and public API queries; scaffold output writes a Cairo file in the current directory]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
