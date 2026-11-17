## Description:

返利信息实时提醒工具，追踪高返商品限时活动、返利到账状态、优惠券过期预警，确保不错过任何省钱机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and deal-seeking users use this skill to receive rebate, price-drop, coupon-expiration, order-status, and withdrawal-threshold reminders for watched products and rebate accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification channels may expose rebate, coupon, or order details if SMS, email, or third-party messaging integrations are connected without clear opt-in and disable controls.

Mitigation: Confirm notifications are opt-in for each channel, use only rebate or coupon accounts the user is comfortable connecting, allow easy disabling, and avoid sending sensitive order details through SMS or email unless the integration is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/rebate-alert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted rebate reminder messages with notification details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product names, rebate rates, rebate amounts, order identifiers, links, urgency labels, and account balances when supplied by the user or connected services.]

## Skill Version(s):

0.1.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
