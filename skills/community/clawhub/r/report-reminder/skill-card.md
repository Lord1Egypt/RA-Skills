## Description:

On workdays, checks whether today's daily report exists and contains substantive content, then outputs a reminder mentioning the configured recipient if it is missing or incomplete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bounding-elk](https://clawhub.ai/user/bounding-elk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team operations agents use this skill to check a configured daily-report file path on weekdays and remind the responsible person when the report is absent, empty, or placeholder-only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured daily-report path may not match the installing workspace's report location.

Mitigation: Confirm or update /data/reports/daily/YYYY-MM-DD.md before scheduling reminders.

Risk: Scheduled reminders may mention the wrong person or use language that is not appropriate for the team.

Mitigation: Review the mention target and localize the reminder text before enabling a recurring schedule.

## Reference(s):

- [README.md](README.md)
- [ClawHub skill page](https://clawhub.ai/bounding-elk/skills/report-reminder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and plain reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic report content generation; reminder output is limited to the configured missing-or-incomplete report condition.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
