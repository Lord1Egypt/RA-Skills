## Description:

本地日报/周报生成工具，基于 JSON 工作数据生成结构化 Markdown 报告，支持日报、周报、指标表格和风险提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and team leads use this skill to turn structured JSON work data into daily or weekly Markdown reports for sharing or recordkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated daily or weekly reports can be incomplete or misleading if the JSON input is stale, sparse, or incorrectly categorized.

Mitigation: Review the generated Markdown before sharing it and confirm that completed work, plans, risks, and metrics match the source data.

Risk: Documentation mentions sending or recurring automation, but the inspected implementation only generates local Markdown output.

Mitigation: Treat scheduling, sending, recipients, and external delivery as separate configuration that requires explicit review and confirmation.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/report-maker-cn)
- [ClawHub publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report text with optional JSON input data and command-line parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily or weekly report generation, optional target date, optional JSON data file input, and optional risks or metrics sections.]

## Skill Version(s):

1.5.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
