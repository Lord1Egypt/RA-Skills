## Description:

Create a Google Docs post-mortem, schedule a Google Calendar review, and notify via Chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create a post-mortem document, schedule a review meeting, and notify a Google Chat space after an incident.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe writes to Google Workspace and may expose incident details to selected recipients.

Mitigation: Confirm the incident name, document contents, calendar attendees, meeting time, and Chat space before execution.

Risk: Placeholder values or inaccurate post-mortem details could create misleading records or notifications.

Mitigation: Replace placeholders with reviewed incident details and inspect the generated Google Docs, Calendar, and Chat commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-post-mortem-setup)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [shell commands, markdown, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-docs, gws-calendar, and gws-chat skills.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
