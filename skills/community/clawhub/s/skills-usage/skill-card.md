## Description:

Counts installed Claude Code skill usage over a selected time range and presents a Markdown/TUI-style usage report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akira82-ai](https://clawhub.ai/user/akira82-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to review how often installed skills are invoked across today, the past 7/30/90 days, or all available history. It helps summarize local skill adoption with ranked counts and visual bar charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broad local Claude conversation history across global and project files, which may contain confidential prompts, source code, secrets, or client data.

Mitigation: Review the skill before installing and use it only where scanning local Claude history is acceptable.

Risk: The skill does not provide a clear pre-scan consent prompt or a way to limit scanning to selected projects or files.

Mitigation: Treat the report as local aggregate usage data and avoid sharing the output when even skill names or usage patterns could disclose sensitive work.

## Reference(s):

- [Skill Usage on ClawHub](https://clawhub.ai/akira82-ai/skills/skills-usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown report with table-style text and visual bar charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for a time range and prints the generated report directly.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
