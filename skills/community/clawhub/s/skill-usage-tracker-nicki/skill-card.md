## Description:

技能调用记录与统计分析。自动追踪所有技能调用，无需用户操作。支持日/周/月/季/年维度的技能使用统计报告。安装后直接使用，无需配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[superuser-fank](https://clawhub.ai/user/superuser-fank)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users can use this skill to maintain local skill-call records and produce daily, weekly, monthly, quarterly, or yearly usage summaries. It is intended for skill usage visibility rather than business analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic session-history scanning and persistent logging may record usage information without clear user control.

Mitigation: Install only after review, prefer explicit opt-in event-based logging, and require clear disable and deletion controls.

Risk: Local usage records can reveal which skills were used and may include free-form notes.

Mitigation: Keep the usage data local, review stored records periodically, and avoid recording sensitive notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superuser-fank/skills/skill-usage-tracker-nicki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text usage reports with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON records and supports time-windowed summaries for day, week, month, quarter, and year.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
