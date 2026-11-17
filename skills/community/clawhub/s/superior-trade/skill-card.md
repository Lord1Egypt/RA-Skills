## Description:

Deprecated Superior Trade skill that redirects users to @superior-ai/superiortrade while still documenting API-key access for backtesting and live trading deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kan2k](https://clawhub.ai/user/kan2k)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this deprecated ClawHub skill to identify the moved Superior Trade package or, if intentionally kept installed, to manage Superior Trade backtests and live trading deployments with their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deprecated package still has authority to create or start live trading deployments that can affect real funds.

Mitigation: Prefer the replacement package, confirm API key scope with Superior Trade, backtest first, and require explicit confirmation before any live start, stop, or delete operation.

Risk: API key exposure could authorize backtests and live deployments.

Mitigation: Read SUPERIOR_TRADE_API_KEY only from the agent environment or credential manager and never ask users to paste secrets into chat.

Risk: Incorrect wallet, balance, or deployment status assumptions can mislead users before trading.

Mitigation: Verify balances, wallet status, and deployment state through current API calls before reporting them or starting deployment.

## Reference(s):

- [Superior Trade account portal](https://account.superior.trade)
- [Replacement ClawHub skill](https://clawhub.ai/superior-ai/superiortrade)
- [Published ClawHub skill page](https://clawhub.ai/kan2k/skills/superior-trade)
- [Superior Trade API](https://api.superior.trade)
- [Hyperliquid public info API](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API request examples and configuration or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPERIOR_TRADE_API_KEY for protected Superior Trade operations.]

## Skill Version(s):

1.5.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
