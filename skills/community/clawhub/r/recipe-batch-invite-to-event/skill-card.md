## Description:

Add a list of attendees to an existing Google Calendar event and send notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace automation users use this recipe to batch-add attendees to an existing Google Calendar event and send the corresponding event notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding attendees with sendUpdates set to all sends Google Calendar notifications to affected recipients.

Mitigation: Confirm the calendar event ID and attendee list before patching the event, then verify the attendee list after the update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-batch-invite-to-event)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and gws-calendar skill; commands modify an existing Google Calendar event and send updates to attendees.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
