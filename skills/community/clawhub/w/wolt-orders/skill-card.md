## Description:

Discover restaurants with advanced filters, place single or group orders on Wolt.com, reorder past favorites, track order status, contact support about delays, and send order updates to Slack or other connected channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dviros](https://clawhub.ai/user/dviros)

### License/Terms of Use:


## Use Case:

External users use this skill to browse Wolt restaurants, build carts, place confirmed food orders, track deliveries, and route order updates or support summaries to connected channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a browser session that may expose Wolt login, delivery address, order, and saved payment context.

Mitigation: Use a trusted browser profile and confirm the delivery address, payment method, items, fees, total, and ETA before checkout.

Risk: The skill can place orders and contact support on the user's behalf.

Mitigation: Require explicit user approval before final checkout, placing an order, or sending a support message.

Risk: Order tracking links and support summaries may be sent to Slack or other connected channels.

Mitigation: Confirm the destination channel and shared content before posting tracking links or support conversation summaries.

## Reference(s):

- [ClawHub Wolt Orders skill page](https://clawhub.ai/dviros/skills/wolt-orders)
- [Wolt](https://wolt.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, browser actions]

**Output Format:** [Markdown summaries, structured lists or tables, checkout confirmations, tracking updates, and channel notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access; final checkout and support-message actions require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
