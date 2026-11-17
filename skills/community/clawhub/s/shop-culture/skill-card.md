## Description:

Enables AI agents to browse lifestyle, wellness, and gift products, create multi-chain crypto or x402 checkout orders for the For the Cult store, apply eligible CULT token discounts, and track shipments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bythecult](https://clawhub.ai/user/bythecult)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to find products, compare purchase options, create checkout requests, and track physical orders through the For the Cult store API. It is suited to agent-assisted shopping workflows where the user remains in control of shipping details, wallet signing, and payment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through real purchases, cryptocurrency payment flows, and sharing shipping information.

Mitigation: Use a runtime that requires explicit user approval before submitting shipping details, displaying payment addresses, signing wallet messages or transactions, or sending crypto payments.

Risk: Some checkout instructions may not consistently gate payment-related steps with fresh user confirmation.

Mitigation: Require manual confirmation for every checkout and payment step unless the user has set a narrow, trusted spending budget.

Risk: Using wallet addresses for discounts can link on-chain activity to an order.

Mitigation: Explain the privacy tradeoff before using wallet-based discounts and only send wallet proof when the user explicitly agrees.

## Reference(s):

- [For the Cult API Endpoint Reference](artifact/references/API.md)
- [Checkout Request Body](artifact/references/CHECKOUT-FIELDS.md)
- [Error Handling Reference](artifact/references/ERRORS.md)
- [For the Cult Store](https://forthecult.store)
- [ClawHub Skill Listing](https://clawhub.ai/bythecult/skills/shop-culture)

## Skill Output:

**Output Type(s):** [guidance, API calls, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces shopping, checkout, payment, and order-status instructions for an agent; does not itself execute payments or store secrets.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact frontmatter lists 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
