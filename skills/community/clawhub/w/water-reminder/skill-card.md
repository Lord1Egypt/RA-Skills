## Description:

A health and wellness skill to remind the user to drink water and stay hydrated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinghaojia](https://clawhub.ai/user/yinghaojia)

### License/Terms of Use:


## Use Case:

External users use this skill to receive hydration prompts, track water intake when requested, and get guidance for setting up recurring water reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring reminders may require cron or heartbeat setup that persists beyond the current conversation.

Mitigation: Only configure recurring reminders after the user explicitly asks for them and understands the persistence involved.

Risk: Hydration tracking can write daily intake details to memory logs.

Mitigation: Record intake only when the user opts into tracking and provides the amount to log.

Risk: The skill may provide occasional hydration prompts that some users may find intrusive.

Mitigation: Use the skill only when the user asks for reminders, tracking, or hydration support.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command or configuration suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest optional daily memory logging or recurring reminder setup only when the user asks for tracking or scheduling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
