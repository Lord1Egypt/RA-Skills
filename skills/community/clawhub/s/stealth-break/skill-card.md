## Description:

Provides discreet break suggestions and macOS notification reminders for eye rest, posture movement, breathing, and other short wellness breaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-qianchen](https://clawhub.ai/user/ryan-qianchen)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to ask for short work-break suggestions and to set macOS notification reminders for periodic wellness breaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add persistent cron-based macOS reminder jobs without enough scoping, removal guidance, or containment.

Mitigation: Before allowing setup, review the exact cron entry and osascript command, confirm the reminder frequency, and record how to list and remove the cron job later.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-qianchen/skills/stealth-break)
- [Publisher profile](https://clawhub.ai/user/ryan-qianchen)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown or plain text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose cron-based macOS notification setup after confirming reminder type and frequency.]

## Skill Version(s):

1.0.0 (source: server release metadata; package.json lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
