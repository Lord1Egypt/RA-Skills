## Description:

Backtest and deploy trading strategies on Superior Trade's managed cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading developers use this skill to configure, backtest, and operate Superior Trade strategies on Hyperliquid with a platform-managed trading wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can manage live trading and move real USDC inside the Superior Trade and Hyperliquid flow.

Mitigation: Require explicit, transaction-specific confirmation before starting live deployments, deposits, sub-account transfers, account changes, deployment deletion, or portfolio exits.

Risk: Live actions can affect real balances and open positions.

Mitigation: Verify balances, open positions, wallet source, deployment status, and strategy sizing immediately before execution.

Risk: Credential exposure would grant high-impact trading authority within the platform scope.

Mitigation: Use only the SUPERIOR_TRADE_API_KEY environment credential and avoid displaying, logging, or storing secrets in agent output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superior-ai/skills/superior-trade-hyperliquid)
- [Superior Trade account portal](https://account.superior.trade)
- [Superior Trade API endpoint](https://api.superior.trade)
- [Hyperliquid public info endpoint](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, code snippets, shell commands, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API calls that create or manage backtests, deployments, portfolio deposits, and position exits.]

## Skill Version(s):

4.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
