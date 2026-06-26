## Description: <br>
Connects to a WooCommerce store via the OpenClaw Connector Lite plugin to fetch orders and products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magnum-opus-v1](https://clawhub.ai/user/magnum-opus-v1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External store operators and developers use this skill to let an agent check WooCommerce connection health, retrieve order details, and search product inventory through a configured WordPress store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return WooCommerce order and customer data to an agent session. <br>
Mitigation: Install it only for agents and operators authorized to view that store data, and avoid order lookups in shared or untrusted conversations. <br>
Risk: The store secret authorizes signed requests to the configured WordPress endpoint. <br>
Mitigation: Protect OPENCLAW_STORE_SECRET like an API key, rotate it when access changes, and configure OPENCLAW_STORE_URL only for an HTTPS WordPress site you control. <br>
Risk: A misconfigured store URL or inactive plugin can cause failed or misleading store lookups. <br>
Mitigation: Use the store_status tool to verify the connection before relying on order or product results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magnum-opus-v1/wooclaw-lite) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text status, order, and product summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCLAW_STORE_URL and OPENCLAW_STORE_SECRET; responses may include WooCommerce order and customer data.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact package.json is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
