## Description:

Use when managing todos, tasks, projects, or kanban boards via Taskleef.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xatter](https://clawhub.ai/user/xatter)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent manage Taskleef todos, projects, subtasks, and kanban boards through the Taskleef CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external Taskleef CLI that uses the user's Taskleef API key.

Mitigation: Install only from a trusted source, prefer a pinned release or verified checksum, avoid running setup as root, and limit exposure of TASKLEEF_API_KEY.

Risk: The skill supports destructive commands such as deleting tasks or projects and clearing kanban columns.

Mitigation: Require explicit user confirmation with exact item IDs or unambiguous names before delete, project delete, or board clear actions.

## Reference(s):

- [Taskleef website](https://taskleef.com)
- [ClawHub skill page](https://clawhub.ai/xatter/skills/taskleef)
- [Taskleef CLI installer source](https://raw.githubusercontent.com/Xatter/taskleef/main/taskleef-cli/todo)
- [jq Linux x86_64 download](https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64)
- [jq Linux ARM64 download](https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-arm64)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the Taskleef CLI and requires TASKLEEF_API_KEY, todo, curl, and jq.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
