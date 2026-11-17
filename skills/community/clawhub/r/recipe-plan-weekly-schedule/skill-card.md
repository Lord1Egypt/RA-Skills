## Description:

Review your Google Calendar week, identify gaps, and add events to fill them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and other Google Workspace users use this recipe to review their weekly Google Calendar availability, identify open blocks, and add a planned event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can read Google Calendar availability and create a calendar event.

Mitigation: Confirm the Google account, calendar scope, and event details before running the gws commands.

Risk: The example free/busy and insert commands use fixed dates.

Mitigation: Edit the date range, start time, and end time for the intended week before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-plan-weekly-schedule)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-calendar skill; example commands should be edited before use.]

## Skill Version(s):

1.0.12 (source: server release metadata; skill source metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
