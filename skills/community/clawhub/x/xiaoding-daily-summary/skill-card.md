## Description:

Generates a Chinese daily learning summary that includes OpenClaw token usage and saves it as a dated Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks for a daily summary or token statistics, producing a concise Chinese learning report with token usage and task status. It is intended for OpenClaw users who want a persistent dated Markdown record of daily progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a persistent dated Markdown file and may update an existing summary for the same day.

Mitigation: Review the target date and existing daily summary before running it when prior notes must be preserved.

Risk: The generated report includes OpenClaw token usage totals.

Mitigation: Avoid sharing the generated daily summary where operational usage details should remain private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-daily-summary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown daily summary plus concise text status and token totals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or updates a dated memory/YYYY-MM-DD.md file under the OpenClaw workspace.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
