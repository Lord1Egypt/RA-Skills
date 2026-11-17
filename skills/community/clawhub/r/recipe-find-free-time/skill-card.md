## Description:

Query Google Calendar free/busy status for multiple users to find a meeting slot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, assistants, and scheduling agents use this recipe to compare Google Calendar availability across multiple attendees and select a shared meeting slot. It also shows how to create an event after the slot is chosen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can create calendar events even though it is described as finding free time.

Mitigation: Use it only with an agent that asks before running the calendar insert command and lets the user verify attendees, title, start time, and end time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-find-free-time)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown recipe with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-calendar skill.]

## Skill Version(s):

1.0.13 (source: ClawHub release metadata; artifact frontmatter metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
