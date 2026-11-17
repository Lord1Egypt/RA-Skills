## Description:

Trade security tokens on the X platform — check balances, place orders, view market data, and review trade history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seineruo](https://clawhub.ai/user/seineruo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an assistant to the X trading API for account review, market monitoring, order placement or cancellation, and trade-history reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive account, balance, position, transaction, and trade-history data through the configured API key.

Mitigation: Use the narrowest available API-key permissions, prefer read-only credentials for monitoring, and avoid using the skill in shared conversations.

Risk: The skill can place and cancel trading orders, which may create financial loss if a request is misunderstood or unauthorized.

Mitigation: Confirm every order or cancellation explicitly, verify symbol, side, order type, quantity, and price, and require extra review for large orders.

Risk: A leaked X_TRADING_API_KEY could expose account data or trading capability.

Mitigation: Never print, log, or repeat the API key, and rotate the key immediately if exposure is suspected.

## Reference(s):

- [x trade ClawHub page](https://clawhub.ai/seineruo/skills/x-trade)
- [seineruo publisher profile](https://clawhub.ai/user/seineruo)
- [X Trading API application page](https://xtrading.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown responses with API request guidance and tabular account, market, order, or history summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include bilingual English or Chinese responses, timestamps for market data, and portfolio or transaction tables.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
