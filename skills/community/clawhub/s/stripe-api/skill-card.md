## Description:

Guides agents through Stripe administration for customers, subscriptions, invoices, products, prices, and payments using managed OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and administer a connected Stripe account, including customers, billing, payments, and event-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial writes can affect live charges, refunds, invoices, subscriptions, or records.

Mitigation: Default to read-only operations; verify test versus live mode, target IDs, amounts, and endpoint, then obtain explicit user approval for each write.

Risk: A broad Stripe connection or unnecessary credential exposure can increase the impact of misuse.

Mitigation: Use CLI/OAuth with the least-privileged account and scopes, confirm the connection before requests, and avoid raw HTTP unless the CLI is unavailable.

Risk: Automated payment events can continuously forward customer and cardholder information.

Mitigation: Require approval for destinations and forward only fields needed by the workflow, not full payment payloads or credentials.

## Reference(s):

- [Stripe skill on ClawHub](https://clawhub.ai/byungkyu/skills/stripe-api)
- [Maton](https://maton.ai)
- [Stripe trigger reference](references/stripe/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a Maton account; writes require explicit user approval.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
