## Description:

Alipay Open Platform integration guide for payment-product selection, sandbox testing, RSA2 signing, async-notification handling, and common error triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select an Alipay payment product, plan sandbox integration, handle RSA2 signing and asynchronous notification verification, and triage common Alipay Open Platform errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment product availability, fees, API details, and compliance requirements may differ by merchant, industry, or current Alipay policy.

Mitigation: Confirm commercial terms and production requirements in Alipay's official console and documentation before relying on the guidance for live payments.

Risk: Incorrect signing, notification verification, idempotency, or amount checks can cause payment failures, duplicate order handling, or incorrect reconciliation.

Mitigation: Use official SDKs where possible, test end-to-end in the sandbox, verify Alipay public-key signatures, enforce idempotency by order ID, and compare notified amounts against local orders.

Risk: Static integration guidance can become stale as platform behavior and product eligibility change.

Mitigation: Treat the skill as implementation guidance, not an authoritative contract, and re-check current Alipay documentation before production changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/zhifubao)
- [Publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions, Code]

**Output Format:** [Markdown guidance with integration checklists, troubleshooting tables, and API method names.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static guidance; does not execute commands, request credentials, or access external systems.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
