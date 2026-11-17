## Description:

Sends hydration and movement reminders every 45 minutes from 8:00 to 23:00 to promote healthy work habits and prevent prolonged sitting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renchzhao](https://clawhub.ai/user/renchzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users use this skill to receive recurring hydration, movement, and eye-rest reminders during configured working hours. It supports healthier work routines during long sessions by tracking the last reminder time locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reminder schedule may not match the user's intended day if the fixed 8:00-23:00 GMT+8 window is not appropriate.

Mitigation: Confirm the desired reminder window before installing or enabling the skill.

Risk: The skill stores the last reminder time and chat/session ID in a local OpenClaw state file to send recurring reminders.

Mitigation: Review the local state file behavior and keep session identifiers protected according to the user's environment policy.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with reminder text, JSON state examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local reminder state for recurring notifications.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
