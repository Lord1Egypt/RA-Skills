## Description:

Solana whale copy trading bot that tracks wallets, simulates or executes copy trades through Jupiter and Pump.fun routing, scans arbitrage opportunities, monitors token launches, and sends Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youthaiagent](https://clawhub.ai/user/youthaiagent)

### License/Terms of Use:

ISC

## Use Case:

External developers and crypto trading operators use this skill to set up a Solana copy-trading workflow that can watch a target wallet, run paper-trading simulations, scan arbitrage opportunities, and optionally execute live swaps after operator review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The live-trading path handles private keys and transaction signing, which can put funds at risk.

Mitigation: Use watch-only or paper mode by default; if live mode is enabled, use only a dedicated low-balance burner wallet.

Risk: Automated crypto trading can execute losing or unintended trades when routing, price impact, liquidity, or token safety checks are wrong or incomplete.

Mitigation: Keep strict per-trade and open-position limits, validate transactions before signing, and add tested live exit controls before using real funds.

Risk: External API, RPC, and alerting dependencies can fail, rate-limit, or return stale data.

Mitigation: Monitor failures, test behavior in paper mode, and require operator review before relying on alerts or live execution.

## Reference(s):

- [API setup](references/api-setup.md)
- [Trading concepts](references/trading-concepts.md)
- [ClawHub skill page](https://clawhub.ai/youthaiagent/skills/solana-copy-trader)
- [Publisher profile](https://clawhub.ai/user/youthaiagent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript source artifacts, environment-variable configuration, console logs, Telegram alert text, and JSON-like analysis reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal operation depends on external Solana, Helius, Jupiter, Pump.fun, CoinGecko, and Telegram services configured by the operator.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
