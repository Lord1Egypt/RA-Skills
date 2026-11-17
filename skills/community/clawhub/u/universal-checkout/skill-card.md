## Description:

Discover, buy, track, and return real products from Amazon, Walmart, Target and almost any other US online retailer through the Zinc API (zinc.com). Needs no account to begin — the agent mints its own test key, then earns a live key and a $5 starter credit once its operator approves it. Pay from a pre-funded wallet, per request over MPP or x402, or with a Stripe Link card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a5huynh](https://clawhub.ai/user/a5huynh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to discover products, place operator-approved purchases, track orders, and request returns through Zinc's API.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Live orders send the operator's name, address, and phone number to Zinc and spend real money; searches also cost money.

Mitigation: Before buying, confirm the item, maximum purchase total, separate order fee, and payment account; never invent an address, and keep the live API key private.

## Reference(s):

- [Agent Sandbox Quickstart](https://www.zinc.com/docs/v2/agent-sandbox/quickstart.md)
- [Going Live](https://www.zinc.com/docs/v2/agent-sandbox/going-live.md)
- [MPP Payments](https://www.zinc.com/docs/v2/mpp.md)
- [Retailer Accounts](https://www.zinc.com/docs/v2/retailer-accounts.md)
- [Create Order API](https://www.zinc.com/docs/v2/api-reference/orders/create-order.md)
- [Get Order API](https://www.zinc.com/docs/v2/api-reference/orders/get-order.md)
- [Error Handling](https://www.zinc.com/docs/v2/api-reference/introduction/error-handling.md)
- [references/errors.md](references/errors.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with curl commands and JSON API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
