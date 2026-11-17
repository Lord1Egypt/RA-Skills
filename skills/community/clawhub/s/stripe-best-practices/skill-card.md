## Description:

Best practices for building Stripe payment integrations

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifoster01](https://clawhub.ai/user/ifoster01)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for guidance on Stripe payment, subscription, billing, and Connect integration choices, including migrations away from legacy APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guidance could be applied as authorization to handle live payment data or make Stripe account changes.

Mitigation: Treat the skill as general integration guidance and require appropriate operational approval before handling live payment data or changing account configuration.

Risk: Stripe-specific recommendations may be over-applied to non-Stripe billing questions.

Mitigation: Use a more narrowly scoped skill or explicit instructions when the task is not about Stripe billing or payments.

Risk: Raw PAN handling carries PCI compliance obligations.

Mitigation: Advise PCI compliance proof before recommending workflows that involve raw card-number handling or processor PAN migration.

## Reference(s):

- [Stripe payment method integration options](https://docs.stripe.com/payments/payment-methods/integration-options)
- [Stripe Payments API tour](https://docs.stripe.com/payments-api/tour)
- [Stripe go-live checklist](https://docs.stripe.com/get-started/checklist/go-live)
- [Migrate from Charges API to PaymentIntents](https://docs.stripe.com/payments/payment-intents/migration/charges)
- [Migrate from Card Element to Payment Element](https://docs.stripe.com/payments/payment-element/migration)
- [Design a Billing subscriptions integration](https://docs.stripe.com/billing/subscriptions/designing-integration)
- [Stripe Connect integration recommendations](https://docs.stripe.com/connect/integration-recommendations)
- [PAN data migration](https://docs.stripe.com/get-started/data-migrations/pan-import)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown or plain-text recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Knowledge-only guidance; no executable code, persistence, or hidden data access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
