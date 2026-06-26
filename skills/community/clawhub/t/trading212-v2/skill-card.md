## Description: <br>
Analyzes Trading212 portfolio, generates daily summaries with P&L and top gainers/losers, makes trade proposals based on configurable rules, and can place orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nandichi](https://clawhub.ai/user/nandichi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to review Trading212 portfolio performance, inspect dividends and order history, generate rule-based trade or rebalancing proposals, and execute explicitly confirmed orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access brokerage account data and place Trading212 orders. <br>
Mitigation: Keep demo mode enabled by default, require explicit user confirmation before any execution, and show the exact order details before placing an order. <br>
Risk: Live trading mode can place real-money orders if enabled. <br>
Mitigation: Use live mode only after deliberate user direction and clearly warn that the order affects real funds. <br>
Risk: Trading212 API credentials are required for account access. <br>
Mitigation: Store API credentials securely in the required environment variables and avoid exposing them in prompts, logs, or generated summaries. <br>
Risk: Portfolio snapshots may be written locally. <br>
Mitigation: Treat snapshot files as account-sensitive data and store them only in an appropriate local directory. <br>


## Reference(s): <br>
- [Trading212 Skill Reference](artifact/reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nandichi/trading212-v2) <br>
- [Publisher Profile](https://clawhub.ai/user/nandichi) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON from skill commands, normally summarized by the agent as concise Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include portfolio values, positions, P&L, proposals, order results, dividends, order history, watchlist alerts, allocation analysis, and structured errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
