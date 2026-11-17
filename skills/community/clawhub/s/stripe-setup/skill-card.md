## Description:

Add Stripe payments to any agent-built app, including checkout sessions, subscription billing, webhook handling, customer portal setup, and test-mode validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferrentinomj-dev](https://clawhub.ai/user/ferrentinomj-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Stripe one-time payments, subscription checkout, webhook handling, subscription access checks, and customer billing portal flows to agent-built web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment integrations can expose secrets or enable unintended live charges if configured carelessly.

Mitigation: Start with Stripe test-mode keys, keep secret keys server-side, and switch to live keys only after completing the release checklist.

Risk: Stripe retries webhook deliveries, which can duplicate fulfillment or entitlement changes without durable idempotency.

Mitigation: Store processed webhook event IDs in a database or Redis before production use.

Risk: The setup includes package installation commands that may require elevated privileges.

Mitigation: Review sudo package-install commands before running them and pin application dependencies.

## Reference(s):

- [Stripe API Reference for Python](https://stripe.com/docs/api?lang=python)
- [Stripe Checkout Sessions API](https://stripe.com/docs/api/checkout/sessions)
- [Stripe Webhook Event Types](https://stripe.com/docs/api/events/types)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Stripe Customer Portal](https://stripe.com/docs/billing/subscriptions/customer-portal)
- [ClawHub Skill Page](https://clawhub.ai/ferrentinomj-dev/skills/stripe-setup)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code blocks, shell commands, and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable Python helper functions for Stripe checkout, billing portal sessions, subscription lookup, customer lookup, and webhook dispatch.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
