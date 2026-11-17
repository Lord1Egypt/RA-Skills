## Description:

Tiny Python CLI tool to manage Google Calendar events from the command line: list, add, update, and delete events via the Calendar API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwings](https://clawhub.ai/user/xwings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a Python-based Google Calendar CLI for listing, creating, updating, and deleting calendar events. It is suitable when an agent needs command-line guidance or execution patterns for Google Calendar workflows using OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses long-lived Google OAuth credentials and refresh tokens.

Mitigation: Store credentials in environment variables or a managed secret store, avoid command-line credential flags, and limit use to a Google account and calendar appropriate for agent access.

Risk: The CLI can update or delete live calendar events.

Mitigation: Require explicit user confirmation before running update or delete commands and review target event IDs before execution.

Risk: Calendar reads may expose sensitive event details to an agent session.

Mitigation: Use only calendars whose event data is acceptable for agent access and avoid granting broader calendar access than the workflow requires.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xwings/skills/py-googlecalendar-cli)
- [Publisher profile](https://clawhub.ai/user/xwings)
- [Project homepage](https://github.com/xwings/py-googlecalendar-cli)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Calendar API v3 endpoint](https://www.googleapis.com/calendar/v3)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google OAuth client credentials, a refresh token, and a calendar ID supplied through environment variables or CLI flags.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
