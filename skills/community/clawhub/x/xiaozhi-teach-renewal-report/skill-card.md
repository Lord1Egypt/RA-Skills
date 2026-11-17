## Description:

帮助独立教师依据学员的学习记录生成阶段报告、梳理进展并草拟续课沟通内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

面向独立教师，用于根据单名学员的相关学习记录整理阶段报告、总结进展并准备续课建议与话术草稿。家长版内容须先通过授权检查。

### Deployment Geography for Use:

China (mainland)

## Known Risks and Mitigations:

Risk: The skill reads minors’ longitudinal learning records and may prepare parent-facing content.

Mitigation: Identify one learner, read only report-related records, and check parent-sharing consent before generating a parent version; check emotion-sharing consent for classroom-state details.

Risk: ClawScan reports medium confidence because two references remain unresolved.

Mitigation: Review those references and the skill’s requirements before installing if they are relevant to your use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-renewal-report)
- [阶段报告模板](artifact/references/stage-report-templates.md)
- [续课沟通话术](artifact/references/renewal-communication-scripts.md)
- [掌握度与授权词汇](artifact/shared/vocab.md)
- [教师工作空间数据结构](artifact/shared/solo-teacher-workspace.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Chinese Markdown reports and draft communication text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only supported learner records; unsupported figures are omitted.]

## Skill Version(s):

2.12.7 (source: server release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
