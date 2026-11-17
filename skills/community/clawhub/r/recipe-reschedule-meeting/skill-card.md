## Description:

Move a Google Calendar event to a new time and automatically notify all attendees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace users and agents use this recipe to locate a Google Calendar event, reschedule it to a new start and end time, and notify attendees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe modifies a real Google Calendar event and can notify all attendees.

Mitigation: Before running the patch command, verify the event ID, start time, end time, timezone, and attendee notification setting.

Risk: Using the wrong Google Workspace account or calendar could reschedule the wrong meeting.

Mitigation: Confirm the active gws account and calendar context before fetching or patching the event.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-reschedule-meeting)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and the gws-calendar skill.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
