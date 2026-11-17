## Description:

Manage tasks with persistent SQLite storage, including creation, retrieval, updates, deletion, status tracking, and priority filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makkzone](https://clawhub.ai/user/makkzone)

### License/Terms of Use:

MIT License

## Use Case:

Developers, agents, and workflow users can use this skill to maintain a persistent local task list with status and priority fields for personal task tracking, lightweight project tracking, and automated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data is stored in a local tasks.db SQLite file.

Mitigation: Use the skill only where local SQLite storage is acceptable, and avoid storing sensitive task titles or descriptions unless the local data handling is appropriate for the workflow.

Risk: Delete commands remove task records without an extra confirmation prompt.

Mitigation: Review task identifiers before deletion and document deletion behavior for users or agents that call the skill.

## Reference(s):

- [Task ToDo ClawHub Skill Page](https://clawhub.ai/makkzone/skills/task-todo)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands]

**Output Format:** [Structured Python dictionaries from agent methods and plain text command-line output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task records include id, title, description, status, priority, created_at, and updated_at fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
