## Description:

Connects to a WooCommerce store via the WPClaw Connector plugin to fetch orders and products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magnum-opus-v1](https://clawhub.ai/user/magnum-opus-v1)

### License/Terms of Use:


## Use Case:

Store operators, developers, and authorized agents use this skill to check WooCommerce order details, search products by name or SKU, and verify the WPClaw Connector plugin connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed customer order data can be exposed through a shared store secret without built-in user authorization.

Mitigation: Install only for trusted store operators or admin-only agents, add backend caller authorization, and redact unnecessary customer fields.

Risk: Store credentials and requests may be exposed if the connector is configured without HTTPS or with broad credentials.

Mitigation: Require HTTPS in WPCLAW_STORE_URL, use narrowly scoped credentials where possible, and pin dependencies with a reviewed lockfile before production use.

Risk: Automated access to store endpoints can create operational abuse or excessive request volume.

Mitigation: Add backend rate limits and monitor connector usage before allowing production agent access.

## Reference(s):

- [WPClaw Connector README](README.md)
- [ClawHub skill page](https://clawhub.ai/magnum-opus-v1/skills/wpclaw-lite)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Plain text status, order, and product search summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WPCLAW_STORE_URL and WPCLAW_STORE_SECRET environment variables to call a configured WooCommerce store.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
