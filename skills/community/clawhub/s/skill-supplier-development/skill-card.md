## Description:

面向SQE与供应商质量经理的低绩效供应商帮扶提升计划生成技能；以诊断-措施-跟踪-验证闭环产出可落地的帮扶计划文档（txt+md）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

SQE teams and supplier quality managers use this skill to structure improvement plans for low-performing suppliers, including diagnosis, corrective actions, responsibilities, milestones, tracking, and verification. It is intended for Chinese-language supplier development workflows where real supplier performance data is provided by the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier performance data may be sensitive if included in generated plans.

Mitigation: Provide only supplier information that is approved for use in generated reports and internal workflows.

Risk: The skill describes running scripts/build_report.py, but that script was not included in the inspected artifact.

Mitigation: Verify the script source and output directory before allowing an agent to run it.

Risk: Supplier metrics, targets, and root-cause conclusions can be misleading if invented or unsupported.

Mitigation: Require user-provided performance data and keep unknown targets or unsupported values marked for completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-supplier-development)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Server-resolved GitHub import](https://github.com/duding-engicool/skill-supplier-development)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown and plain text supplier improvement plan with an optional shell command for report generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates supplier help-plan documents and marks missing performance targets or unsupported values for user completion.]

## Skill Version(s):

0.1.0 (source: server release evidence); artifact frontmatter reports 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
