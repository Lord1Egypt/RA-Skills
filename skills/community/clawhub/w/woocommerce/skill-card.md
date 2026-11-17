## Description:

Helps agents manage WooCommerce products, orders, customers, settings, and store automations through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and developers use this skill to inspect and, with explicit approval, update WooCommerce catalog, order, customer, and store resources or set up related automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Store changes, refunds, and settings updates can affect orders or customers.

Mitigation: Confirm the exact store, target, payload, and effect with the user before each write.

Risk: Customer and order responses can expose personal information.

Mitigation: Retrieve and display only the fields needed for the task.

Risk: Webhooks and trigger destinations can forward future events until removed.

Mitigation: Review the destination and event scope before approval, and remove unneeded automations.

Risk: Broad access or long-lived API keys increase exposure if credentials are compromised.

Mitigation: Review requested scopes and prefer the OAuth CLI login over API keys.

## Reference(s):

- [WooCommerce skill release](https://clawhub.ai/byungkyu/skills/woocommerce)
- [WooCommerce REST API documentation](https://woocommerce.github.io/woocommerce-rest-api-docs/)
- [Maton](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON API results]

**Output Format:** [Text and Markdown with shell commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Store responses depend on the connected account and its granted permissions.]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
