## Description:

Use Stripe's live REST API for authenticated account inspection and operational lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect a live Stripe account with a user-provided secret key, list common billing and payment objects, search customers, and retrieve known objects through read-only commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents need a Stripe secret key to query a live account, and leaked live keys can expose account data.

Mitigation: Use a restricted Stripe key where possible, keep keys in STRIPE_SECRET_KEY, do not paste or commit live keys, and rotate any secret shared in chat or files.

Risk: Read-only Stripe responses can contain customer, payment, invoice, payout, dispute, and webhook details.

Mitigation: Review command output before sharing or storing it and redact sensitive business or customer data.

Risk: Future write actions against Stripe could move money or change billing state.

Mitigation: Keep this release to read-only commands and require explicit user confirmation before adding or running write actions.

## Reference(s):

- [Stripe API Objects and Workflows](references/objects-and-workflows.md)
- [Stripe API base endpoint](https://api.stripe.com/v1)
- [ClawHub skill page](https://clawhub.ai/stanestane/skills/stripe-api-readonly)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses STRIPE_SECRET_KEY from the local environment and performs read-only Stripe API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
