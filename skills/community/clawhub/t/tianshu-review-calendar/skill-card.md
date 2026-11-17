## Description:

Tianshu Review Calendar spreads course topics across the days before an exam and produces a printable Markdown review schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Students use this skill to turn an exam date and a list of course topics into a day-by-day pre-exam review calendar. It is suited to end-of-term review planning, not hourly reminders or personalized study diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a user-supplied topic file when --file is used.

Mitigation: Pass only files that contain study topics intended for the review calendar.

Risk: Very long or unrealistic schedule lengths may produce unwieldy review plans.

Mitigation: Use normal schedule lengths and review the generated calendar before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangshengli0421/skills/tianshu-review-calendar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown table with schedule notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local text output only; no network, credential, persistence, or privileged behavior is reported.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
