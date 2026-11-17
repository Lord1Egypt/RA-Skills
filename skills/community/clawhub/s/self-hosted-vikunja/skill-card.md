## Description:

Interact with a self-hosted Vikunja task management instance via its REST API to create, update, delete, and list tasks, projects, and labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bydavid](https://clawhub.ai/user/bydavid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and self-hosted Vikunja users use this skill to manage tasks, projects, labels, reminders, due dates, recurring tasks, and bulk task completion through an agent-driven REST API workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Vikunja credentials and authentication tokens.

Mitigation: Use only an HTTPS Vikunja URL, prefer a limited-permission Vikunja account, avoid running login where stdout is logged, and protect or remove the cached token file.

Risk: The skill can delete task and project data.

Mitigation: Require explicit confirmation before task or project deletion.

Risk: The skill can modify live task, project, label, reminder, due date, recurring task, and bulk-completion state.

Mitigation: Review the target instance, project IDs, task IDs, and requested operation before executing mutating commands.

## Reference(s):

- [Vikunja API Reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Python CLI helper that reads Vikunja connection settings from configuration or environment variables.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
