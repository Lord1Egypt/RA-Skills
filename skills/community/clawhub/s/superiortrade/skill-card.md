## Description:

Backtest and deploy trading strategies on Superior Trade's managed cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading users use this skill to generate, backtest, tune, and deploy trading strategies on Superior Trade for Hyperliquid and Aerodrome/Base markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can enable real-money trading and account-affecting actions, including moving assets between managed accounts and closing positions.

Mitigation: Require explicit confirmation before live deployment, transfer, stop, delete, or exit actions, and prefer a backtesting-only or narrowly scoped key if Superior Trade offers one.

Risk: Private keys or seed phrases could be mishandled if requested or entered during setup.

Mitigation: Use only SUPERIOR_TRADE_API_KEY through the environment or credential manager; do not request, log, store, or display wallet private keys or seed phrases.

Risk: Trading strategy guidance and backtest results can be misleading or financially risky if treated as guarantees.

Mitigation: Review strategy assumptions, run backtests before deployment, use out-of-sample checks where practical, and present live trading decisions for user confirmation.

## Reference(s):

- [Superior Trade ClawHub Skill](https://clawhub.ai/superior-ai/skills/superiortrade)
- [Superior-AI Publisher Profile](https://clawhub.ai/user/superior-ai)
- [Superior Trade Account](https://account.superior.trade)
- [Superior Trade API](https://api.superior.trade)
- [Hyperliquid Public Info API](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON payloads, Python strategy code, shell/API command examples, and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or manage backtests and deployments when the user provides the required API key and authorizes the action.]

## Skill Version(s):

4.4.6 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
