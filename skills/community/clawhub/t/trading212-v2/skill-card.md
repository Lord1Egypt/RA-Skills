## Description:

Analyzes Trading212 portfolios, generates daily summaries with P&L and top gainers/losers, makes trade proposals from configurable rules, can place orders, and also supports dividends, order history, watchlist alerts, allocation analysis, and rebalancing proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nandichi](https://clawhub.ai/user/nandichi)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect Trading212 portfolio performance, dividends, order history, watchlists, allocation, and rule-based trade proposals. It can also submit confirmed Trading212 orders when configured with account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real-money Trading212 orders when live trading is enabled.

Mitigation: Keep TRADING212_DEMO=true unless live trading is intended, require explicit user confirmation before order execution, and clearly review the symbol, side, quantity, and order type before running execute_trade.

Risk: The skill requires credentials that may allow access to account data and trading authority.

Mitigation: Use restricted or read-only credentials where possible, install only when that account access is acceptable, and avoid placing secrets in shared parent .env files.

Risk: The skill can read external rules configuration and write portfolio snapshots using broad paths.

Mitigation: Review TRADING212_RULES_PATH and TRADING212_SNAPSHOT_DIR before use, and relocate them to controlled paths when running in shared or sensitive environments.

## Reference(s):

- [Trading212 Skill Reference](artifact/reference.md)
- [Trading212 Demo API Base URL](https://demo.trading212.com/api/v0)
- [Trading212 Live API Base URL](https://live.trading212.com/api/v0)
- [ClawHub Skill Page](https://clawhub.ai/nandichi/skills/trading212-v2)
- [ClawHub Publisher Profile](https://clawhub.ai/user/nandichi)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance, Shell commands, Configuration]

**Output Format:** [Structured JSON from command output, typically summarized by the calling agent as readable text or markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Modes include summary, propose, execute_trade, dividends, history, watchlist, and allocation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
