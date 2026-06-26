## Description: <br>
Monitors WooCommerce processing orders, copies billing details into missing shipping addresses, and emits one alert per new order for downstream automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WooCommerce operators and automation developers use this skill to monitor processing orders, fill missing shipping addresses from billing data, and emit one-line signals for fulfillment or alerting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation can update live WooCommerce order shipping data, including customer address fields, without a dry-run or confirmation step. <br>
Mitigation: Use a dedicated least-privilege WooCommerce key, test on staging first, review the billing-to-shipping field mapping, and add dry-run or approval controls before production scheduling. <br>
Risk: Write failures may not be handled reliably before downstream alerts or deduplication state are recorded. <br>
Mitigation: Add PUT response checks, logging, and failure handling so orders are only marked alerted after the shipping update path succeeds or is explicitly skipped. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zero2ai-hub/skill-woocommerce-order-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and stdout status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces HEARTBEAT_OK when no new orders are found and NEW_ORDER_ID lines for newly detected orders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
