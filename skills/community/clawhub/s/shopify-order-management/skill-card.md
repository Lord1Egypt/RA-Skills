## Description: <br>
Shopify order lifecycle management with new order handling, status sync, low-stock alerts, abandoned cart recovery, and daily sales reports. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
External developers, Shopify operators, and agency teams use this skill to import n8n workflows for order logging, status synchronization, inventory alerts, abandoned-cart recovery, and daily sales reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflows handle Shopify customer and order data and export selected fields to Google Sheets. <br>
Mitigation: Use least-privilege Shopify and Google Sheets credentials, restrict sheet access, minimize stored fields, and define retention rules before deployment. <br>
Risk: Abandoned-cart recovery emails may create consent, unsubscribe, suppression, and regional compliance obligations. <br>
Mitigation: Enable the recovery workflow only after verifying consent checks, unsubscribe handling, suppression lists, and applicable regional email requirements. <br>
Risk: Webhook-triggered order handling depends on correct Shopify signature validation and secret configuration. <br>
Mitigation: Set SHOPIFY_WEBHOOK_SECRET, test invalid-signature rejection, and rotate credentials if webhook URLs or secrets are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhmalvi/shopify-order-management) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [New Order Handler workflow](artifact/workflows/01-new-order-handler.json) <br>
- [Order Status Sync workflow](artifact/workflows/02-order-status-sync.json) <br>
- [Low Stock Alert workflow](artifact/workflows/03-low-stock-alert.json) <br>
- [Abandoned Cart Recovery workflow](artifact/workflows/04-abandoned-cart-recovery.json) <br>
- [Daily Sales Report workflow](artifact/workflows/05-daily-sales-report.json) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Code, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance plus n8n JSON workflow files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Shopify, Google Sheets, and SMTP credentials plus environment variables for store URL, access token, webhook secret, admin email, and low-stock threshold.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and _meta.json report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
