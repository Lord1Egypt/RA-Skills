## Description:

QuickTaxReturn guides users through simple 2025 U.S. federal tax preparation by collecting tax document data, performing step-by-step calculations, and routing complex cases to DIY filing, CPA handoff, or advisory support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vajih](https://clawhub.ai/user/vajih)

### License/Terms of Use:

MIT-0

## Use Case:

Taxpayers use this skill to organize simple 2025 federal return information, estimate filing outcomes, and identify when a CPA handoff is appropriate. It is limited to federal tax preparation guidance and escalates state, business, investment-sale, foreign-income, and other complex cases.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can collect or summarize highly sensitive tax, identity, banking, and IRS PIN information during preparation or CPA handoff.

Mitigation: Do not enter full SSNs, bank account numbers, IRS IP PINs, or similar secrets in chat; redact handoff notes and use a secure CPA portal for sensitive values.

Risk: The CPA handoff uses a configured commercial referral link rather than neutral provider selection.

Mitigation: Present the referral as a configured commercial referral, disclose that users may choose any qualified CPA or enrolled agent, and avoid implying independent provider matching.

Risk: Tax calculations and eligibility guidance may be incomplete or outdated for complex or changing tax situations.

Mitigation: Verify calculations against original tax documents and current IRS guidance, and escalate business, investment-sale, multi-state, foreign-income, K-1, and other complex cases to a licensed tax professional.

## Reference(s):

- [QuickTaxReturn ClawHub Skill Page](https://clawhub.ai/vajih/skills/quicktaxreturn)
- [Core Skill Behavior](artifact/SKILL.md)
- [Escalation Config](artifact/escalation-config.md)
- [CPA Intake Package Template](artifact/intake-template.md)
- [Tax Rules](artifact/tax-rules.md)
- [IRS Rev. Proc. 2024-40](https://www.irs.gov/pub/irs-drop/rp-24-40.pdf)
- [IRS Notice 2024-80](https://www.irs.gov/pub/irs-drop/n-24-80.pdf)
- [IRS Free File](https://www.irs.gov/freefile)
- [IRS Direct File](https://directfile.irs.gov)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text with Markdown summaries and intake-package templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include step-by-step tax calculations, filing summaries, CPA referral details, and structured handoff notes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
