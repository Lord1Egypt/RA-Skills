## Description:

Task scheduling and dispatching for task boards. Use when setting up periodic task dispatch, checking for dispatchable tasks, creating subagents to execute tasks, or verifying task completion. Supports task board APIs like ClawBoard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cccaptain0129](https://clawhub.ai/user/cccaptain0129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to monitor task-board APIs, dispatch eligible automated tasks to subagents, verify completion signals and deliverables, and update task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring dispatch authority can let an agent repeatedly spawn subagents and modify task-board state.

Mitigation: Use reviewed task sources, manual approval for sensitive tasks, bounded schedules, and task-board permissions limited to the intended workspace.

Risk: The setup flow may execute an unpinned remote installer.

Mitigation: Install from a reviewed pinned release or commit before enabling scheduled dispatch.

Risk: Access tokens may be copied into workspace environment files.

Mitigation: Use least-privilege tokens, protected secret storage, and avoid committing workspace environment files.

## Reference(s):

- [Task Dispatch skill page](https://clawhub.ai/cccaptain0129/skills/task-dispatch)
- [Configuration reference](references/config.md)
- [Subagent dispatch template](references/dispatch-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, bash, Python, and completion-signal code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cron configuration JSON, task dispatch prompts, API request examples, status-update guidance, and verification checklists.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
