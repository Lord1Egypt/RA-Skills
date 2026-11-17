## Description:

Helps subscription businesses monitor churn risk and produce retention guidance, dunning message templates, downgrade recommendations, and price-sensitivity flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, lifecycle marketers, retention teams, and subscription commerce teams use this skill to diagnose renewal and dunning risk, draft failed-payment recovery sequences, and design downgrade or pause options before cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer billing exports and churn data can contain sensitive customer or payment-related information.

Mitigation: Avoid sharing raw exports unless needed, minimize fields, and anonymize sensitive churn data where possible.

Risk: Subscription disclosure and cancellation rules can vary by jurisdiction.

Mitigation: Use qualified counsel for regulated subscription-law questions and do not treat the skill as legal advice.

Risk: Dunning timing or retention offers may be wrong if they are not matched to the merchant's processor, retry rules, grace period, timezone, and compensation policy.

Mitigation: Verify platform retry settings, merchant policy, timezone, eligibility rules, and finance approval before sending customer-facing messages.

## Reference(s):

- [Subscription churn and dunning playbook](artifact/references/subscription_churn_playbook.md)
- [ClawHub skill page](https://clawhub.ai/rijoyai/skills/sub-churn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown playbooks, tables, and copy-pasteable message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include merge-field placeholders for customer, plan, payment, downgrade, pause, and support details.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
