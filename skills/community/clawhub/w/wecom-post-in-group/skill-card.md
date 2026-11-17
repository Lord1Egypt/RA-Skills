## Description:

Sets up scheduled or recurring content pushes to WeChat Work group webhooks with daily, weekly, monthly, and advanced schedule patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckyethan](https://clawhub.ai/user/luckyethan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and operations teams use this skill to configure recurring WeChat Work group notifications, validate webhook access, format messages, and create scheduled automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs and keys are reusable secrets and may be exposed through prompts, logs, shell history, or user-facing output.

Mitigation: Treat webhook URLs and keys like passwords: mask them in user-visible summaries, avoid storing them in logs or shell history, and rotate any key that may have been exposed.

Risk: The skill can send live test messages and create recurring active posts to a WeChat Work group.

Mitigation: Require clear user confirmation before any test send or scheduled automation is created, and verify the target group, message content, schedule, and active status before enabling it.

## Reference(s):

- [Schedule Patterns Reference](references/schedule_patterns.md)
- [ClawHub skill page](https://clawhub.ai/luckyethan/skills/wecom-post-in-group)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and automation configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live WeChat Work webhook validation or post commands when the user provides a webhook.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
