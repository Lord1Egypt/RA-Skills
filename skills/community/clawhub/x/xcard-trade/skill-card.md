## Description: <br>
Trade crypto perpetual futures on XCard — view positions, place orders, monitor funding rates, and manage margin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seineruo](https://clawhub.ai/user/seineruo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to operate XCard crypto perpetual futures workflows, including market review, position and margin checks, order execution, and trade-history reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive account, order, trade, and transaction history through an authenticated XCard API key. <br>
Mitigation: Use a restricted API key, avoid withdrawal permissions, and install only when the publisher is trusted. <br>
Risk: The skill can perform live account changes such as placing, canceling, or modifying orders and changing leverage. <br>
Mitigation: Require explicit manual confirmation before every order, cancellation, modification, leverage change, or account-transaction-history request. <br>
Risk: Crypto perpetual futures use leverage and can expose users to liquidation and funding-fee losses. <br>
Mitigation: Review liquidation price, leverage, margin, funding rate, order side, size, and price before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seineruo/xcard-trade) <br>
- [XCard API key application page](https://xcard.com/api) <br>
- [XCard API base endpoint](https://api.xcard.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API Calls, configuration] <br>
**Output Format:** [Markdown summaries, tables, and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XCARD_TRADE_API_KEY for authenticated XCard API workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
