## Description:

Trade security tokens on the XCard platform: check balances, place orders, view market data, and review trade history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seineruo](https://clawhub.ai/user/seineruo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent interact with XCard trading APIs for account balances, portfolio positions, market data, order placement, order cancellation, and trade history review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private financial account data and trade history.

Mitigation: Use a scoped or revocable XCard API key, avoid exposing the key, and treat balances, positions, transactions, and history as private.

Risk: The skill can place or cancel trading orders.

Mitigation: Require explicit user confirmation for order placement and cancellation, repeat order details before execution, and warn when an order value exceeds 10% of available balance.

Risk: Broad activation could route unrelated requests into financial account or trading actions.

Mitigation: Use the skill only for explicit XCard trading intent and ask clarifying questions when symbols, quantities, prices, or date ranges are ambiguous.

## Reference(s):

- [XCard API access](https://xcard.com/api)
- [XCard API base URL](https://api.xcard.com/v1)
- [ClawHub skill page](https://clawhub.ai/seineruo/skills/xcard-trading)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown text with tables, concise trading guidance, and API-backed account, market, order, and history responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XCARD_API_KEY; market data responses should include timestamps, and portfolio/history responses may include private financial information.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
