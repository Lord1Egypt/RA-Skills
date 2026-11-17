## Description:

Monitors WooCommerce processing orders, copies billing details into missing shipping addresses, and emits one alert per new order for downstream automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

WooCommerce store operators and automation developers use this skill to keep processing orders ready for fulfillment and send one downstream notification per new order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically update live WooCommerce order shipping addresses using stored API credentials.

Mitigation: Use a least-privilege WooCommerce API key, require an HTTPS store URL, protect the credentials file, test on staging first, and add dry-run/apply controls plus response checks before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zero2ai-hub/skills/skill-woocommerce-order-guard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, and plain-text output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script output may include HEARTBEAT_OK or NEW_ORDER_ID lines.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
