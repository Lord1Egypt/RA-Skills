## Description:

Connects to a WooCommerce store via the OpenClaw Connector Lite plugin to fetch orders and products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magnum-opus-v1](https://clawhub.ai/user/magnum-opus-v1)

### License/Terms of Use:


## Use Case:

External developers and store operators use this skill to let an agent check WooCommerce order status, search products, and verify connection health through the OpenClaw Connector Lite WordPress plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Store secrets and customer or order data can be exposed if the skill is configured for stores where agent access is inappropriate.

Mitigation: Protect OPENCLAW_STORE_SECRET like a credential and grant agents access only to stores and order data they are allowed to inspect.

Risk: The security assessment says the connector does not enforce HTTPS or strong replay-resistant request signing.

Mitigation: Use only HTTPS WooCommerce URLs and install from a locked, reviewed dependency set before connecting production stores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magnum-opus-v1/skills/wooclaw-lite)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text order, product, and connection status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WooCommerce customer, order, product, stock, and pricing details returned by the configured store.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
