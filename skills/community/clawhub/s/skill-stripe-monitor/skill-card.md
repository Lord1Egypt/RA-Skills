## Description:

Stripe revenue dashboard in your agent - MRR, churn, new subscriptions, failed payments, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordo-tech](https://clawhub.ai/user/ordo-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and business teams use this skill to ask an agent for read-only Stripe revenue, subscription, churn, failed-payment, product, and balance summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A full live Stripe secret key can expose more account capability than a read-only monitoring workflow needs.

Mitigation: Use a restricted Stripe key with read-only permissions for customers, subscriptions, invoices, charges, products, and prices.

Risk: Revenue, payment, and customer-related details may be sent to external destinations through summaries, alerts, or webhooks.

Mitigation: Enable Telegram summaries, automatic alerts, or webhooks only for private destinations approved to receive sensitive business data.

Risk: Webhook use requires handling Stripe webhook signing secrets and a reachable OpenClaw instance.

Mitigation: Configure webhook verification with STRIPE_WEBHOOK_SECRET and use polling when a public webhook endpoint is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ordo-tech/skills/skill-stripe-monitor)
- [Stripe API keys](https://dashboard.stripe.com/apikeys)
- [Stripe API](https://api.stripe.com/v1/...)
- [Stripe status](https://status.stripe.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only Stripe metric summaries and setup guidance; requires operator-provided Stripe credentials.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
