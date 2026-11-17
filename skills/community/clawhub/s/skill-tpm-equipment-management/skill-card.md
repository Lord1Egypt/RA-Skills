## Description:

设备管理领域 TPM（全员生产维护）的辅助技能，聚焦具体可执行模块：六大损失分析、自主保全七步推进、计划保全、OPL 一点课、设备点检基准书、八大支柱轻量引导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Maintenance, reliability, and operations teams use this skill to turn equipment data, maintenance records, descriptions, or photos into TPM module deliverables such as loss analysis tables, autonomous-maintenance plans, preventive-maintenance plans, OPL drafts, inspection standards, and pillar guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Equipment, maintenance, or production data may contain sensitive operational information.

Mitigation: Provide only the data needed for the TPM task and remove confidential identifiers when possible.

Risk: Referenced knowledge files and an optional build script are not included in the inspected artifact, so output quality may vary with the agent's general knowledge or future package contents.

Mitigation: Review generated TPM deliverables against internal maintenance standards before use.

Risk: Missing enterprise-specific equipment parameters, standards, or thresholds can make outputs incomplete.

Mitigation: Keep unknown enterprise-specific fields explicitly marked for completion instead of filling them with assumptions.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-tpm-equipment-management)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-tpm-equipment-management)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure Markdown deliverables in the conversation; enterprise-specific missing values are marked for user completion.]

## Skill Version(s):

1.0.0 (source: frontmatter); ClawHub release version 0.1.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
