## Description:

Task Quest adds XP, levels, streaks, achievements, and brief progress reporting to smart-tasks based task management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgkim311](https://clawhub.ai/user/dgkim311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and task-management users use this skill to add a lightweight gamification layer to an existing smart-tasks workflow, with the agent calculating XP, maintaining streaks, tracking achievements, and appending concise progress notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains persistent local gamification state about completed tasks, XP, streaks, achievements, and history.

Mitigation: Install only when persistent task-gamification tracking is desired, and review the generated task-quest state files before relying on them.

Risk: Workspace integration changes can alter agent startup, heartbeat, and briefing behavior.

Mitigation: Review and approve the AGENTS.md, HEARTBEAT.md, and cron prompt diffs before applying them.

Risk: The deactivation behavior affects how game elements are shown and may affect ongoing tracking expectations.

Mitigation: Confirm the intended active/inactive behavior before installation and document any local policy for pausing or retaining tracking.

Risk: Some user-facing templates are Korean-language by default.

Mitigation: Adapt the templates and examples to the workspace locale before deployment if Korean output is not desired.

## Reference(s):

- [Task Quest on ClawHub](https://clawhub.ai/dgkim311/skills/task-quest)
- [Workspace Integration Guide](references/workspace-integration.md)
- [Task Quest Game Mechanics](references/mechanics.md)
- [Task Quest Achievement Catalog](references/achievements.md)
- [Task Quest Theme System](references/themes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local state-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise task-completion notes, quest status summaries, and workspace integration guidance; initialization creates local Markdown state files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
