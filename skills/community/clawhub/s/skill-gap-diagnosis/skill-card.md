## Description:

Analyzes multi-dimensional insurance business data to calculate premium gaps, required cases, urgency and ease tags, priority order, and a diagnosis summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimolc](https://clawhub.ai/user/nimolc)

### License/Terms of Use:

MIT

## Use Case:

Insurance agents, managers, and business operations teams use this skill to diagnose shortfalls across performance, campaign, honor, renewal, customer-growth, and skill dimensions. It is intended for multi-dimensional gap and progress analysis rather than single-metric lookup or general chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to business performance, campaign, honor, renewal, customer-growth, skill, assessment, and allowance data.

Mitigation: Install only in environments where the skill is approved to access those data categories.

Risk: Security evidence flags a mismatch between the skill's diagnosis-only promise and recommendation-oriented examples or retrieval hints.

Mitigation: Before production use, remove recommendation-oriented content or route advice-like outputs through the intended governed advice workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nimolc/skills/skill-gap-diagnosis)
- [Diagnosis prompt reference](artifact/references/diagnosis.md)
- [Input schema](artifact/schema/input.json)
- [Output schema](artifact/schema/output.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Traditional Chinese diagnosis prose with structured JSON gap indicators and retrieval hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Amounts are represented in HKD; output includes data-as-of dates and ranking freshness notes when rank data is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
