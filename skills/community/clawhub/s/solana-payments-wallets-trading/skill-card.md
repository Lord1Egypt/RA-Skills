## Description: <br>
Helps agents use a Solana CLI to manage wallets, send SOL or tokens, trade and swap assets, stake, lend, provide liquidity, trade prediction markets, pay x402 resources, and inspect portfolio state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solanaguide](https://clawhub.ai/user/solanaguide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to propose Solana CLI commands for payments, wallet operations, token trading, DeFi positions, prediction markets, x402 payments, and portfolio checks. It is best suited to supervised workflows where the user reviews commands before any transaction affecting funds is executed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose Solana operations that affect real funds, including transfers, swaps, staking, borrowing, liquidity provision, prediction trades, and x402 payments. <br>
Mitigation: Use a dedicated low-balance wallet, require human confirmation for fund-affecting commands, and preview with --dry-run or --quote-only where supported. <br>
Risk: Wallet keys and security configuration are stored under ~/.sol/ and could be exposed if an agent or other tool is granted filesystem access to that directory. <br>
Mitigation: Keep ~/.sol/ off-limits to agents and other tools; interact through the CLI rather than reading key or config files directly. <br>
Risk: Default permissions allow fund-affecting actions unless the user configures restrictions. <br>
Mitigation: Configure permissions, transaction limits, token allowlists, and address allowlists, then review with sol config status and lock settings before agent-assisted use. <br>
Risk: Token symbols can be ambiguous and routing, prices, rates, and market outcomes can change quickly. <br>
Mitigation: Verify token mint addresses and quotes before execution, prefer explicit mint addresses for unfamiliar assets, and keep transaction sizes appropriate for the risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solanaguide/solana-payments-wallets-trading) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Trading commands](artifact/references/trading-commands.md) <br>
- [Wallet commands](artifact/references/wallet-commands.md) <br>
- [Staking commands](artifact/references/staking-commands.md) <br>
- [Lending commands](artifact/references/lending-commands.md) <br>
- [Liquidity pool commands](artifact/references/lp-commands.md) <br>
- [Prediction market commands](artifact/references/prediction-commands.md) <br>
- [x402 fetch commands](artifact/references/fetch-commands.md) <br>
- [Portfolio commands](artifact/references/portfolio-commands.md) <br>
- [JSON output format](artifact/references/json-output-format.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run, quote-only, permission, limit, and allowlist guidance before fund-affecting commands.] <br>

## Skill Version(s): <br>
0.3.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
