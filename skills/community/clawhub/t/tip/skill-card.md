## Description:

Recognizes a user's intent to tip, collect and validate a tip amount, confirm the amount with the user, and call the payment skill to complete the payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sayxxx](https://clawhub.ai/user/sayxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External agents use this skill when a user expresses an explicit tipping, appreciation, or gift intent. It collects a positive amount up to 10000 yuan, asks for confirmation, and passes payment parameters to the payment skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create payment orders without clearly binding or confirming who receives the money.

Mitigation: Require an explicit tipping intent and show the verified recipient and amount before creating or presenting a payment order.

Risk: Users could follow untrusted payment links.

Mitigation: Only display payment links from trusted payment systems and review returned payment links before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sayxxx/skills/tip)
- [Publisher profile](https://clawhub.ai/user/sayxxx)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text or Markdown conversation responses with payment skill parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects amount, validates amount > 0 and amount <= 10000, confirms with the user, and passes amount, order_type, and description to the payment skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
