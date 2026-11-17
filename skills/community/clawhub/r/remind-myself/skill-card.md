## Description:

Set a one-shot reminder delivered via Telegram at a specific time or after a duration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to schedule one-shot reminders that are delivered through Telegram after a relative delay or at an absolute time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted reminder text may be interpreted as arbitrary local shell commands through the documented execution pattern.

Mitigation: Invoke the reminder script with structured arguments or robust escaping, and review reminder text before scheduling.

Risk: Reminder text is sent to Telegram and the workflow depends on a Telegram chat ID stored in the expected OpenClaw workspace file.

Mitigation: Use this skill only when the user accepts Telegram delivery and has configured the intended chat ID.

Risk: Absolute-time handling uses a fixed Europe/Paris timezone in the artifact workflow.

Mitigation: Confirm the user's timezone before scheduling reminders for absolute times.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spideystreet/skills/remind-myself)
- [OpenClaw binary requirement](artifact/SKILL.md)
- [Reminder setup and usage](artifact/README.md)
- [Release changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, a configured Telegram channel, and a Telegram chat ID available to the reminder script.]

## Skill Version(s):

1.0.6 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
