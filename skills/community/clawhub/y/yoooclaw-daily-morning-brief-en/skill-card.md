## Description:

Organizes recent notifications into a concise morning report with key information, today's to-dos, missed items, follow-ups, decisions, risks, and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill to turn recent work and personal notifications into an actionable morning briefing. It highlights schedule-impacting updates, missed responses, follow-ups, decisions, and tasks for the current day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query and summarize sensitive work and personal notifications across connected sources.

Mitigation: Limit connected applications and watched groups to the minimum needed for the briefing, and review whether notification access is appropriate before installation.

Risk: The skill runs a local notification search command using user-provided or inferred time ranges.

Mitigation: Use explicit, narrow time windows and validate free-form time ranges before running notification searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-daily-morning-brief-en)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured session text with a Markdown-style morning brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No file is generated; the brief is concise and organized around key information, to-dos, risks, and reminders.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
