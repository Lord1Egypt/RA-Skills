## Description:

只读汇总独立教师的课表、学员跟进、作业、家长沟通和课时信息，生成按优先级排列的每日工作台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

独立教师可用此技能查看每日课程、课前准备、课后反馈、作业跟进、家长沟通和剩余课时，并按记录中的数值信号确定优先事项。输出供教师审阅；工作台仅读取和汇总数据。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The workspace may contain sensitive information about students and guardians.

Mitigation: Use aliases, include only necessary details, respect consent and retention settings, and confirm teaching context before reading student records.

Risk: Field-based risk labels and priorities could be mistaken for a complete assessment of a student's needs.

Mitigation: Show the supporting values and timeframe, keep recommendations for teacher review, and do not present derived labels as subjective judgments.

Risk: The security review was partial because two local references were unavailable to the scanners.

Mitigation: Review the affected references and confirm their content before relying on guidance that depends on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-solo-dashboard)
- [Daily dashboard block templates](artifact/references/daily-dashboard-block-templates.md)
- [Daily dashboard full sample](artifact/references/daily-dashboard-full-sample.md)
- [Dashboard template](artifact/references/dashboard-template.md)
- [Solo teacher workspace schema](artifact/shared/solo-teacher-workspace.schema.json)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown daily dashboard with seven sections, evidence-based risk notes, and three prioritized actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only summary; uses aliases and documented field values, and leaves decisions and external communications to the teacher.]

## Skill Version(s):

2.12.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
