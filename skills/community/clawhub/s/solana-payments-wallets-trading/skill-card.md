## Description:

Helps agents use the Solana Compass CLI to send SOL or tokens, manage wallets, swap and trade tokens, stake SOL, lend or borrow assets, provide liquidity, trade prediction markets, pay x402-protected APIs, configure spending controls, and inspect portfolio performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solanaguide](https://clawhub.ai/user/solanaguide)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill when they want an agent to propose or run Solana CLI commands for wallet operations, payments, trading, DeFi yield actions, prediction markets, x402 API payments, and portfolio review. The skill is best suited for controlled, user-reviewed workflows that use dedicated wallets and explicit spending limits.

### Deployment Geography for Use:

Global, except prediction-market commands may be unavailable from US and South Korea IP addresses.

## Known Risks and Mitigations:

Risk: Commands can move real funds through wallet transfers, swaps, staking, lending, borrowing, liquidity provision, prediction-market trades, and x402 payments.

Mitigation: Use a dedicated low-balance wallet, keep only funds needed for the workflow, require user review for fund-moving commands, and set transaction and daily limits before use.

Risk: Running npx with @latest can execute mutable package versions.

Mitigation: Review the CLI source or install a pinned, verified package version before enabling fund-moving operations.

Risk: Default permissions allow write operations unless disabled.

Mitigation: Disable unneeded permissions such as canFetch, canSwap, canTransfer, canLend, canBorrow, and canPredict, then verify with sol config status and lock the configuration.

Risk: x402 requests can spend USDC and may expose sensitive request content to paid web services.

Mitigation: Run sol fetch with --dry-run first, set a small --max cap, and do not place secrets in request bodies or headers.

Risk: Wallet key files and security configuration are stored under ~/.sol and can be read by software running with filesystem access under the same OS user.

Mitigation: Do not grant agents read or write access to ~/.sol; interact through reviewed sol CLI commands and keep larger holdings outside agent-accessible key files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solanaguide/skills/solana-payments-wallets-trading)
- [Fetch Commands Reference](references/fetch-commands.md)
- [JSON Output Format Reference](references/json-output-format.md)
- [Lending Commands Reference](references/lending-commands.md)
- [LP (Liquidity Pool) Commands Reference](references/lp-commands.md)
- [Portfolio Commands Reference](references/portfolio-commands.md)
- [Prediction Market Commands Reference](references/prediction-commands.md)
- [Staking Commands Reference](references/staking-commands.md)
- [Trading Commands Reference](references/trading-commands.md)
- [Troubleshooting](references/troubleshooting.md)
- [Wallet Commands Reference](references/wallet-commands.md)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 20 plus node and npx; command outputs can be human-readable tables or CommandResult JSON envelopes when --json is used.]

## Skill Version(s):

0.3.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
