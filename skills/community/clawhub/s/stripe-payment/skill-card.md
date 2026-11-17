## Description:

Enables AI assistants to manage Stripe customers, payment intents, subscriptions, invoices, refunds, balances, and webhook verification through the Stripe API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaolfun](https://clawhub.ai/user/gaolfun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent perform Stripe account workflows such as customer setup, payment creation, subscriptions, refunds, invoice lookup, and balance review. It is most appropriate where payment operations are gated by credential scoping, test-mode validation, and explicit confirmation for account-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Stripe credentials can allow real charges, refunds, subscription creation, cancellation, and other account-changing actions.

Mitigation: Use Stripe test mode first, prefer restricted keys, and require explicit confirmation before any account-changing operation.

Risk: Stripe secret keys or webhook secrets can be exposed if used client-side, logged, or shared too broadly.

Mitigation: Keep secrets server-side, avoid logging credentials, and scope credentials to the minimum permissions required.

Risk: Incorrect amount or currency handling can create payments or refunds for the wrong value.

Mitigation: Validate currency and smallest-unit amounts before execution, and show the final amount in human-readable form for confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaolfun/skills/stripe-payment)
- [Stripe API keys](https://dashboard.stripe.com/apikeys)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Stripe testing cards](https://stripe.com/docs/testing#cards)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, SDK code examples, setup steps, and Stripe API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Stripe object IDs, payment statuses, balance summaries, refund details, subscription details, and error remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
