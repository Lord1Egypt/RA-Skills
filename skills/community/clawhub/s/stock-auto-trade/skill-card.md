## Description:

股票交易下单和查询功能。需要提供股票代码、价格、数量等信息。支持买入、卖出、持仓查询、账户查询、撤单等操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangheng3](https://clawhub.ai/user/yangheng3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare local HTTP API calls for stock buy, sell, cancellation, position, account, and order queries after configuring a trusted local trading assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare requests for real stock orders and cancellations through an external trading assistant.

Mitigation: Require manual confirmation in a trusted trading interface before any order or cancellation is sent.

Risk: The artifact uses a public default API key for authenticated requests.

Mitigation: Replace the default API key with a unique strong secret before use.

Risk: The skill depends on an external trading assistant that is not verified by the provided provenance.

Mitigation: Install and use the trading assistant only if its source and behavior can be independently trusted and verified.

Risk: Exposing the trading API beyond the local machine could allow unauthorized financial actions.

Mitigation: Keep the trading assistant API bound to localhost.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangheng3/skills/stock-auto-trade)
- [Publisher profile](https://clawhub.ai/user/yangheng3)
- [Trading assistant download page](https://www.gp998.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown with curl commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a local trading assistant API configured on localhost.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
