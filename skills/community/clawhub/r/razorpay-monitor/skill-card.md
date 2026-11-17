## Description:

Autonomous Razorpay payment monitoring for Indian merchants that tracks daily settlements, detects failed payments, sends WhatsApp/Telegram anomaly alerts, delivers weekly revenue summaries, and connects to the Razorpay API using merchant keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utsavs](https://clawhub.ai/user/utsavs)

### License/Terms of Use:


## Use Case:

External merchants and operators use this skill to monitor Razorpay payment activity, settlements, refunds, disputes, and revenue summaries through an agent. It supports proactive alerts and on-demand payment-status questions without requiring routine dashboard checks.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The agent can read Razorpay payment, settlement, refund, dispute, and limited customer-contact data when configured with merchant API keys.

Mitigation: Install only for intended merchant accounts, use appropriately scoped Razorpay keys where possible, and keep API keys in environment variables rather than messages or logs.

Risk: WhatsApp or Telegram alerts may send operational payment details to unintended recipients if alert destinations are misconfigured.

Mitigation: Confirm all alert recipients before enabling delivery and keep customer emails, phone numbers, and other contact details masked in reports.

Risk: Cron-style polling can create recurring background access to payment data.

Mitigation: Enable daily reports, anomaly polling, and weekly summaries only when recurring monitoring is required.

## Reference(s):

- [Razorpay API](https://api.razorpay.com/v1/)
- [ClawHub skill page](https://clawhub.ai/utsavs/skills/razorpay-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style reports and alerts with inline shell and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked customer-contact fields, payment summaries, settlement status, refund summaries, dispute reminders, and alert thresholds.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
