## Description:

Subscription Sentinel helps an agent inspect recent email receipts, infer subscription billing cycles, alert users about upcoming renewals, and offer cancellation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeysome](https://clawhub.ai/user/joeysome)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill with a trusted OpenClaw workspace to review subscription-related email receipts, track inferred billing schedules, and receive timely renewal or cancellation options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive email and billing data.

Mitigation: Use it only in a private workspace with trusted email access, and protect or delete subscriptions.json when it is no longer needed.

Risk: Cancellation guidance or browser-assisted cancellation can change user accounts or paid services.

Mitigation: Require user approval for each exact service and final cancellation step before taking action.

Risk: Subscription detection and billing-cycle inference may be incomplete or incorrect.

Mitigation: Review detected subscriptions against primary billing records before relying on alerts or cancellation recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeysome/skills/subscription-sentinel)
- [OpenClaw homepage metadata](https://github.com/your-username/SubscriptionSentinel)
- [OpenClaw framework](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown reports with subscription tables, cancellation guidance, and optional JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should match the user's conversation language and are based on available email receipt evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
