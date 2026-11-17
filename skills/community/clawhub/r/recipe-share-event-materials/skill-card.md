## Description:

Share Google Drive files with all attendees of a Google Calendar event.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, workspace administrators, and agents use this skill to share Google Drive materials with attendees of a Google Calendar event and verify the resulting permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drive files may be shared with unintended recipients if the event attendee list includes external guests, groups, or forwarded invitations.

Mitigation: Review the attendee list and file sensitivity before granting access, share only with intended recipients, and remove permissions afterward when access is temporary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-share-event-materials)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-calendar and gws-drive skills.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
