## Description:

帮助公司团队规划团建活动目的地。收集团队成员的偏好（活动类型、预算、时间等），综合分析推荐最佳目的地，并通过flyai查询详细信息。适用于团建规划、集体出游、公司活动等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiguan1](https://clawhub.ai/user/shiguan1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team coordinators use this skill to collect outing constraints and member preferences, compare candidate destinations, and prepare a shareable team outing recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run external flyai CLI searches with team outing details.

Mitigation: Use non-sensitive team details, confirm fly.ai data sharing is acceptable, and prefer a pinned local flyai-cli install with safe argument-based execution.

Risk: The skill instructs agents to create and automatically open an HTML recommendation report.

Mitigation: Ask before creating or opening files, sanitize generated HTML content and links, and review the report before sharing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shiguan1/skills/team-outing-planner)
- [README.md](artifact/README.md)
- [preferences-template.md](artifact/preferences-template.md)
- [html-template.md](artifact/html-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendations with inline shell commands and generated HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local HTML report at ~/team-outing-recommendation.html and open it in a browser when followed.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
