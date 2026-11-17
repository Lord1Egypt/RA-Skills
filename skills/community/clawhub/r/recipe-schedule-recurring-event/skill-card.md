## Description:

Create a recurring Google Calendar event with attendees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to create a recurring Google Calendar meeting on the primary calendar and invite attendees, then verify the event appears in the agenda.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a recurring event on the user's primary Google Calendar and invite an attendee without a clear confirmation step.

Mitigation: Require confirmation of the calendar, event title, start and end time, recurrence rule, attendee list, and notification intent before executing the insert command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-schedule-recurring-event)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command and the gws-calendar skill; commands can create a recurring event on the user's primary Google Calendar.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata); skill metadata version 0.22.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
