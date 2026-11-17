## Description:

Quick Reminders schedules one-shot reminders under 48 hours and delivers the prewritten message through OpenClaw when the timer fires.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lstpsche](https://clawhub.ai/user/lstpsche)

### License/Terms of Use:


## Use Case:

External users and personal-assistant agents use this skill to schedule, list, and cancel short-horizon reminders delivered to a configured messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delayed background delivery jobs may send reminder text later through a configured messaging target.

Mitigation: Use the skill only for non-sensitive reminders and verify the saved delivery target before relying on delivery.

Risk: Stored reminder text and runtime files can expose local reminder contents if file handling is weak.

Mitigation: Prefer a private 0700 runtime directory, mktemp-created message files, and 0600 permissions for reminders.json.

## Reference(s):

- [Quick Reminders on ClawHub](https://clawhub.ai/lstpsche/skills/quick-reminders)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline shell commands and short confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local reminder state and delayed background delivery jobs; pending reminders do not survive machine reboot.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
