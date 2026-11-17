## Description:

Create recurring focus time blocks on Google Calendar to protect deep work hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this recipe to create recurring busy focus-time blocks on a primary Google Calendar, then verify the protected time appears on the agenda.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe creates recurring busy events on the primary Google Calendar, which can block availability if the account, time window, time zone, weekdays, or duration are wrong.

Mitigation: Confirm the target calendar account and recurrence details before execution, then run the agenda verification step after creating the block.

Risk: The example recurrence has no explicit end date, so the focus-time block may continue indefinitely.

Mitigation: Decide whether an end date is required and adjust the recurrence rule before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-block-focus-time)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Google Calendar focus-time blocks through the required gws command and gws-calendar skill.]

## Skill Version(s):

1.0.12 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
