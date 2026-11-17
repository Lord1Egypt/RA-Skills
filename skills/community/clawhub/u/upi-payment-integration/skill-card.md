## Description:

Design and implement robust UPI payment integrations for collect, intent, QR, and autopay mandate flows with webhook handling, idempotency, reconciliation, and RBI-aligned authentication and compliance guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, review, or troubleshoot UPI payment integrations across collect, intent, QR, and recurring mandate flows. It focuses on payment correctness, webhook verification, idempotency, reconciliation, failure handling, and production readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for payment credentials and webhook secrets even though it provides documentation-only guidance.

Mitigation: Use sandbox credentials only when installation requires environment variables, and do not expose production payment keys or webhook secrets to the agent.

Risk: Webhook storage guidance may lead teams to retain sensitive payment headers or payload fields without sufficient controls.

Mitigation: Retain only necessary fields, redact sensitive headers, encrypt restricted data, and define a retention policy before production use.

Risk: Payment regulations, provider APIs, limits, and policies can change after the skill's last verified date.

Mitigation: Confirm current PSP, RBI, and NPCI documentation before production changes, and validate in sandbox or staging before release.

## Reference(s):

- [NPCI UPI Product Overview](https://www.npci.org.in/what-we-do/upi/product-overview)
- [RBI Authentication Mechanisms Directions, 2025](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898)
- [RBI e-Mandate Recurring Transaction Update](https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=12570&Mode=0&fn=9)
- [Razorpay Webhook Behavior and Caveats](https://razorpay.com/docs/webhooks/payments/?preferred-country=IN)
- [Setup](setup.md)
- [Reference](reference.md)
- [Examples](examples.md)
- [Validation Checklist](validation-checklist.md)
- [Failure Handling](failure-handling.md)
- [Launch Playbook](launch-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with checklists, implementation plans, pseudocode, and inline code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides architecture or fix plans, concrete code and database changes, failure-mode checks, and test plans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
