## Description:

Access Stripe directly with a Stripe secret or restricted API key for broad read-only platform queries, especially Connect accounts, application fees, balances, charges, customers, invoices, subscriptions, payouts, transfers, and balance transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgelewi5](https://clawhub.ai/user/georgelewi5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and finance teams use this skill to ask an agent for direct Stripe platform analytics and connected-account reporting without an intermediary gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Stripe credentials can expose sensitive financial and customer data to the agent.

Mitigation: Use the most restricted read-only Stripe key that supports the required reports, keep keys outside git, and avoid unrestricted platform secret keys.

Risk: The covered Stripe areas include payouts, transfers, refunds, and account-change surfaces where misuse could affect live financial operations.

Mitigation: Use this skill for read-oriented analysis only and do not use it for refunds, payouts, transfers, or account changes.

Risk: Stripe keys may be exposed through logs, shell history, or copied command output.

Mitigation: Avoid printing credentials, prefer local secret storage or environment variables, and rotate any key that may have been exposed.

## Reference(s):

- [Stripe API v1 base URL](https://api.stripe.com/v1/)
- [ClawHub skill page](https://clawhub.ai/georgelewi5/skills/stripe-full-read-access)
- [ClawHub publisher profile](https://clawhub.ai/user/georgelewi5)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Stripe API requests and read-oriented reporting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
