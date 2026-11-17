## Description:

Give your AI the power to act in the future. Schedule delayed prompts and one-off reminders that automatically wake the agent up at an exact moment to execute workflows, check systems, or send notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devlumuz](https://clawhub.ai/user/devlumuz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to schedule one-off reminders or delayed agent workflows at precise future times, with enough context for the awakened agent to act without relying on the original conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates OS-level scheduled tasks that can later wake an agent with stored instructions.

Mitigation: Install only where this behavior is intended, run it as an unprivileged user, and review scheduled instructions before creating tasks.

Risk: Reminder text can persist sensitive information until the scheduled task runs.

Mitigation: Avoid putting secrets, credentials, or confidential data in reminder instructions.

Risk: The security evidence flags unsafe command and scheduler control that should be reviewed before installation.

Mitigation: Prefer a revised version that uses spawn or execFile, validates inputs, keeps a private registry of its own jobs, and confirms deletion.

## Reference(s):

- [ClawHub To-Do skill page](https://clawhub.ai/devlumuz/skills/to-do)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and confirmation blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, OPENCLAW_BIN, OPENCLAW_TZ, and native OS scheduling support.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
