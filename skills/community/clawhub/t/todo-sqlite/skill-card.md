## Description:

Manage multi-project todos with SQLite, supporting subtasks, priority and urgency levels, keyword search, time filters, smart sorting, and scheduled reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laoyutang](https://clawhub.ai/user/laoyutang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage local todo projects from a Chinese-language SQLite-backed CLI, including subtasks, deadlines, status updates, searches, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete commands can remove projects or todos and should be treated as irreversible.

Mitigation: Review the target project name or todo ID before running delete-project or delete.

Risk: A disclosed code bug may leave child todos behind after deletion messages.

Mitigation: Check todo listings after deletion when parent-child todo integrity matters.

Risk: Terminal escape or control characters in user-provided titles, notes, or project names may affect terminal display.

Mitigation: Avoid pasting untrusted text into todo titles, notes, or project names.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laoyutang/skills/todo-sqlite)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local SQLite database at ~/.openclaw/workspace/data/todo.db.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
