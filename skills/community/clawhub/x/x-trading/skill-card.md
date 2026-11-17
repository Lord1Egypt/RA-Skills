## Description:

Trade security tokens on the X platform \u2014 check balances, place orders, view market data, and review trade history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seineruo](https://clawhub.ai/user/seineruo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage X platform security-token trading workflows, including account review, market data lookup, order placement or cancellation, and trade-history reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive account, balance, position, order, transaction, and trade-history data.

Mitigation: Use a least-privileged API key and avoid granting account-history or trading permissions unless the workflow requires them.

Risk: The skill can cancel orders and the release security summary notes missing explicit cancellation safeguards.

Mitigation: Manually confirm order cancellations and other sensitive trading actions before allowing the agent to call the API.

Risk: Trading actions can create financial loss if the requested symbol, side, type, quantity, or price is wrong.

Mitigation: Require explicit confirmation of order details and apply the documented large-order warning before placing an order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seineruo/skills/x-trading)
- [X Trading API key application](https://xtrading.com/api)
- [X Trading API base URL](https://api.xtrading.com/v1)
- [Account and portfolio module](artifact/api-account.md)
- [Market data module](artifact/api-market.md)
- [Order execution module](artifact/api-orders.md)
- [Trade history module](artifact/api-history.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls]

**Output Format:** [Markdown responses with API request guidance and tabular account, market, order, or history summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X_TRADING_API_KEY and may handle sensitive account, order, and transaction data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
