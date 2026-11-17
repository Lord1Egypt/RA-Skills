## Description:

Use Stripe's live REST API for authenticated write actions that create or update customers, products, prices, payment links, refunds, subscriptions, and metadata with a STRIPE_SECRET_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to perform authenticated Stripe write operations for live billing workflows, including customer, product, price, payment link, refund, subscription, and metadata changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live Stripe billing and payment changes using the supplied secret key.

Mitigation: Use a restricted Stripe key where possible, require --confirm, preview commands before execution, and verify target object IDs before running writes.

Risk: Refunds and subscription cancellations can directly affect money flow and customer access.

Mitigation: Double-check payment intent, charge, and subscription IDs, and confirm refund amounts, invoice behavior, and proration settings before execution.

Risk: The update_metadata command accepts a broad Stripe API path and is not allowlisted to specific resource types.

Mitigation: Avoid update_metadata unless the exact path has been reviewed and the intended object type is confirmed.

## Reference(s):

- [Stripe API Actions and Safety](references/actions-and-safety.md)
- [Stripe API v1 endpoint](https://api.stripe.com/v1)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STRIPE_SECRET_KEY and --confirm for write actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
