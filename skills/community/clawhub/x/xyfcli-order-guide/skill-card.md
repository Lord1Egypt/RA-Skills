## Description: <br>
Xyfcli Order Guide helps agents place fertilizer orders, query product, inventory, customer, supplier, and address information, and parse order images through the xyfcli CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayafans](https://clawhub.ai/user/mayafans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operational users use this skill to guide an agent through fertilizer ordering workflows, including product and inventory checks, customer and address lookup, order confirmation, order placement, and address updates through xyfcli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a stored order-system token to view customer data and change order or address records. <br>
Mitigation: Install only for trusted publishers and target systems, use a limited and revocable token, and verify customer, address, product, quantity, logistics, and receiver fields before confirming an order. <br>
Risk: Weak secret handling may expose order-system tokens or customer/order details through configuration output or transcripts. <br>
Mitigation: Avoid commands that print configuration in JSON, keep transcripts private, and rotate or revoke tokens after exposure or when access is no longer needed. <br>
Risk: Reusing another customer's address could create privacy and fulfillment issues. <br>
Mitigation: Use another customer's address only when the organization explicitly permits it and the operator has confirmed the intended receiver and delivery details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mayafans/xyfcli-order-guide) <br>
- [Workflow guide](references/workflow_guide.md) <br>
- [CLI quick reference Chinese](references/cli_quickref_chinese.md) <br>
- [Image processing guide](references/image_processing.md) <br>
- [xyfcli scripts README](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline xyfcli shell commands and structured confirmation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the xyfcli binary and a configured order-system base URL and token.] <br>

## Skill Version(s): <br>
1.4.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
