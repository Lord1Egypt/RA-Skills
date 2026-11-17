## Description:

Pulse TODO helps AI agents maintain one workspace TODO.md for commitments, reminders, recurring checks, scheduling, and task selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to make agents capture commitments, maintain a TODO.md, sync scheduled reminders with OpenClaw cron, and choose next tasks by strategic alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to persist tasks and change existing TODO.md or HEARTBEAT.md behavior.

Mitigation: Back up existing TODO.md and HEARTBEAT.md before use, and require confirmation before modifying heartbeat guidance.

Risk: The skill instructs agents to create or remove OpenClaw cron jobs for timed and recurring tasks.

Mitigation: Require confirmation before cron changes and periodically compare TODO.md scheduled entries with the active cron configuration.

Risk: The setup guidance may prompt agents to scan memory or strategy files during migration.

Mitigation: Limit migration to user-approved files and review any imported tasks before they become active.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kagura-agent/skills/pulse-todo)
- [Setup guide](setup.md)
- [TODO template](TODO-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with TODO.md templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent task-management guidance for TODO.md and scheduled OpenClaw cron entries.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
