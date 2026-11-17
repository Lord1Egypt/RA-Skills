## Description:

Payment Integration Expert helps agents produce Stripe payment, subscription, webhook, refund, split-payment, and China payment alternative integration guidance and code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and implement online payment flows for ecommerce and SaaS products, including Stripe PaymentIntent and Subscriptions, webhook verification, refunds and disputes, Connect split payments, and WeChat Pay, Alipay, or UnionPay alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated payment, refund, subscription, webhook, or amount-validation logic may be incorrect for a production money-flow path.

Mitigation: Use test API keys first and manually review refund, subscription cancellation, webhook, and amount-validation logic before production use.

Risk: The skill may suggest SDK installation or execution steps and payment credentials are sensitive.

Mitigation: Confirm exec or install commands before running them, and keep API keys in environment variables or a secret manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/stripe-payment-integrator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, API examples, configuration notes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment API examples, SDK installation commands, webhook handling patterns, and environment variable configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
