## Description:

Shopify order lifecycle management with new order handling, status sync, low-stock alerts, abandoned cart recovery, and daily sales reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

External ecommerce operators, agencies, and developers use this skill to configure n8n workflows that track Shopify orders, synchronize order status, monitor inventory, recover abandoned carts, and send daily sales reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public Shopify webhook may accept unauthenticated order data.

Mitigation: Before enabling the webhook, verify Shopify HMAC signatures against the raw request body and fail closed on missing or invalid signatures.

Risk: The workflows process customer PII and order data in Google Sheets and email.

Mitigation: Define privacy, retention, access-control, opt-out, and deduplication rules before deployment.

Risk: Automated abandoned-cart emails can expose unsafe content or invalid recovery links.

Mitigation: Escape email content and validate recovery URLs before sending customer recovery messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mhmalvi/skills/shopify-order-management)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with n8n workflow JSON and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Shopify, Google Sheets, SMTP, and n8n credentials supplied by the operator.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
