## Description:

Comprehensive SaaS billing guidance for subscriptions, usage-based billing, invoicing, Stripe payments, dunning, proration, and multi-platform payment integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

External SaaS developers and operators use this skill as guidance for planning billing workflows, subscription plans, usage-based charges, invoices, payment integrations, failed-payment recovery, and plan-change proration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is documentation-only and references missing billing commands, so following it directly may fail or create incomplete billing workflows.

Mitigation: Treat it as incomplete documentation, require an inspectable implementation, and review commands before use.

Risk: The quick start suggests passing a Stripe key on a command line.

Mitigation: Use restricted test-mode keys first and provide secrets through safer secret-management mechanisms instead of command-line arguments.

Risk: Connecting production billing data before review could affect payments, invoices, or customer account state.

Mitigation: Validate in sandbox or test accounts before connecting production Stripe, PayPal, or Square data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/saas-billing-system)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-oriented output; review commands and payment-provider setup before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
