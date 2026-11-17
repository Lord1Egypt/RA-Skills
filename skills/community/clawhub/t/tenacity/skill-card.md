## Description:

Autonomous goal completion with checkpoint, resume, and no intermediary confirmation handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[as76](https://clawhub.ai/user/as76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep an agent working through complex or long-running tasks with checkpoint, resume, and completion protocols. It is intended for scoped autonomous execution where the agent pauses only for hard blockers or completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for unattended workspace access and persistent execution authority.

Mitigation: Restrict file and tool access to the specific task scope before use, and require confirmation for destructive or external actions.

Risk: The skill can create durable scheduled execution and continue after restarts.

Mitigation: Disable cron unless explicitly needed, and use clear stop conditions and completion criteria for each task.

Risk: The skill references sending summaries to a hard-coded Telegram recipient.

Mitigation: Remove or replace the hard-coded destination before deployment, and require confirmation for external messages.

Risk: Checkpoint data may persist in a shared temporary directory.

Mitigation: Store checkpoints in a private, validated directory with appropriate access controls.

## Reference(s):

- [Tenacity Standing Orders Template](references/standing-orders-template.md)
- [ClawHub skill page](https://clawhub.ai/as76/skills/tenacity)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and structured checkpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes standing order templates, checkpoint/resume patterns, and completion criteria for autonomous task execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
