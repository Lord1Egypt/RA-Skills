## Description:

Monitor recurring-billing and subscription business health, including pool volatility, churn, and payment failure, then produce dunning and retention email series grounded in compensation psychology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

Subscription operators, lifecycle marketers, and customer-success teams use this skill to review recurring-billing health, track failed renewals, and draft structured dunning or win-back messages. It is intended for subscription contexts with churn, payment-failure, or retention concerns, not one-off transactional receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share sensitive subscription metrics or payment-failure summaries while using the skill.

Mitigation: Provide only the customer and billing data needed for the task, redact raw payment details, and follow internal data-handling policies.

Risk: Retention or dunning messages could promise compensation that operations cannot fulfill.

Mitigation: Confirm approved make-good options before sending messages and avoid promises outside policy.

Risk: Win-back messages may be treated differently from transactional dunning communications.

Mitigation: Review consent, unsubscribe, and jurisdiction-specific email requirements before sending marketing-oriented win-back messages.

## Reference(s):

- [Subscription health, dunning & compensation psychology](references/subscription_playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured tables and email drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces health tables, payment-failure tracking, and multi-message retention or dunning sequences; no executable code is produced by default.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
