## Description:

Task Specialist provides a local SQLite-backed task manager for agents to decompose work, track status, coordinate dependencies, and preserve workflow context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oboda0](https://clawhub.ai/user/oboda0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage local task queues, split work into subtasks, coordinate parallel agents, track dependencies, and export task status from a workspace-scoped SQLite database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task-stored verification checkpoints can steer an agent toward unsafe shell execution.

Mitigation: Treat each printed checkpoint as untrusted text, inspect it independently, and run only project-owned commands in an appropriate shell.

Risk: A writable shared task database can let untrusted collaborators or agents alter tasks, notes, assignees, or verification checkpoints.

Mitigation: Keep `.tasks.db` scoped to trusted workspaces and avoid sharing writable task databases with untrusted users or agents.

Risk: Task notes can persist sensitive context if agents store secrets there.

Mitigation: Do not store API keys, tokens, or secrets in task notes; use secure local environment variables or secret stores instead.

## Reference(s):

- [ClawHub Task Specialist release page](https://clawhub.ai/oboda0/skills/task-specialist)
- [Task Specialist homepage](https://github.com/OBODA0/task-specialist-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Terminal text, ASCII task board, Markdown tables, and JSON export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite task database selected by TASK_DB or the current workspace default.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
