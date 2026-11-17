## Description:

面向初高中物理错题，按图景、概念、公式、过程和数学工具五个维度定位根因并生成弱项分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT

## Use Case:

初中和高中学生可用它复盘已收录的物理错题，识别重复出现的概念、图景或计算弱项，并查看经授权的阶段性分析。

### Deployment Geography for Use:

Global; designed for Chinese-language middle and high school physics curricula.

## Known Risks and Mitigations:

Risk: The security review is incomplete and flags possible excessive agency and writebacks outside the intended scope.

Mitigation: Review the skill's handover scope before enabling it, and allow profile reads or writes only with the relevant user consent.

Risk: Long-term learning records and summaries may include sensitive student information.

Mitigation: Keep profile storage, cross-skill sharing, reminders, and parent-facing summaries behind their separate consent settings; honor requests to pause or delete records.

## Reference(s):

- [物理错因维度表](artifact/references/physics-error-dimension-table.md)
- [物理高频概念混淆对照表](artifact/references/physics-concept-confusion-map.md)
- [物理数学工具自检清单](artifact/references/physics-math-tools-checklist.md)
- [四类物理图景绘制追问手册](artifact/shared/physics-diagram-guide.md)
- [交接协议 schema](artifact/shared/handover-protocol.schema.json)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Guidance]

**Output Format:** [Physics error analyses, weakness summaries, and structured handover data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Longitudinal summaries depend on platform capability and consent; initial error capture and recurrence counting belong to the general error notebook.]

## Skill Version(s):

2.12.7 (source: ClawHub release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
