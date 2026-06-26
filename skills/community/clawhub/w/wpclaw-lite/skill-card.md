## Description: <br>
Connects to a WooCommerce store via the WPClaw Connector plugin to fetch orders and products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magnum-opus-v1](https://clawhub.ai/user/magnum-opus-v1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and store operators use this skill to let an agent check WooCommerce store health, fetch order details, and search products after configuring the WPClaw Connector plugin and required store credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The store secret can authorize access to WooCommerce data if exposed. <br>
Mitigation: Store WPCLAW_STORE_SECRET in a protected secrets mechanism, avoid pasting it into chats or committing it to source control, and rotate it if exposure is suspected. <br>
Risk: Order lookups may return customer or order details into agent responses or logs. <br>
Mitigation: Use the skill only in environments where returned WooCommerce data is appropriate for the agent session, logging policy, and user access level. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/magnum-opus-v1/wpclaw-lite) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text summaries returned by agent tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include WooCommerce order, customer, product, stock, price, and connection-status details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
