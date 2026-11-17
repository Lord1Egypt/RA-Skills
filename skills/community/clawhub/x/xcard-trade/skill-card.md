## Description:

Trade crypto perpetual futures on XCard - view positions, place orders, monitor funding rates, and manage margin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seineruo](https://clawhub.ai/user/seineruo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage XCard crypto perpetual futures workflows, including account review, market data checks, order placement, order changes, funding review, and trade history reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place, cancel, or modify crypto perpetual futures orders and change leverage, which can create immediate financial exposure.

Mitigation: Require the agent to show exact symbol, side, order type, size, leverage, price, and liquidation details, then wait for explicit confirmation before any trade, order cancellation, order modification, or leverage change.

Risk: The skill uses an XCard API key that may expose sensitive balances, positions, orders, trade history, and transaction history.

Mitigation: Use a tightly scoped API key, avoid withdrawal permissions, keep the key in XCARD_TRADE_API_KEY, and never expose, log, or repeat the key in responses.

Risk: High leverage and margin changes can increase liquidation risk.

Mitigation: Warn users about liquidation risk, show estimated liquidation prices for new orders, and give stronger warnings for leverage above 20x or liquidation prices near the current market price.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seineruo/skills/xcard-trade)
- [Publisher Profile](https://clawhub.ai/user/seineruo)
- [XCard API Access](https://xcard.com/api)
- [XCard API Base URL](https://api.xcard.com/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance, Configuration]

**Output Format:** [Markdown summaries, tables, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account balances, positions, orders, trade history, funding information, liquidation warnings, and confirmation prompts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
