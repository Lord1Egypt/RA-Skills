## Description:

面向职业院校技能大赛的全流程备赛AI助手，帮助生成项目方向、PPT大纲、展示剧本和知识点训练计划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pc1335](https://clawhub.ai/user/pc1335)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, competition coaches, and student teams use this skill to prepare for vocational skill contests by generating project plans, PPT outlines, presentation scripts, and training plans. The skill is intended to keep technical, artistic, and comprehensive contest preparation aligned with the relevant contest type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published backend notes expose reusable Dify API keys and a plaintext HTTP endpoint for workflow calls.

Mitigation: Rotate the exposed keys, replace them with user-provided secrets, require HTTPS, and avoid using the documented backend as published.

Risk: User competition materials may be sent to a remote workflow service.

Mitigation: Clearly disclose remote processing and obtain consent before submitting user-provided plans, scripts, team details, or reference materials.

Risk: Generated contest guidance may include incorrect or misleading recommendations.

Mitigation: Review generated project plans, scoring claims, PPT outlines, scripts, and training standards against official competition rules before use.

## Reference(s):

- [赛项规程要点](references/competition-rules.md)
- [展示禁忌清单](references/presentation-taboos.md)
- [技能大赛评分维度与权重](references/scoring-dimensions.md)
- [项目方案输出模板](templates/project-plan-template.md)
- [Dify Workflow调用脚本](scripts/call-dify-workflow.md)
- [ClawHub skill page](https://clawhub.ai/pc1335/skills/skill-contest-prep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and Chinese prose, with optional shell command examples for workflow calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces chained preparation artifacts: project directions, full project plan, PPT outline, presentation script, knowledge map, training schedule, and checklist.]

## Skill Version(s):

1.0.0 (source: release evidence; skill frontmatter version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
