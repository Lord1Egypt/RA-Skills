## Description:

Per-workspace SQLite todo manager (./todo.db) with groups and task statuses (pending/in_progress/done/skipped), operated via {baseDir}/scripts/todo.sh for adding, listing, editing, moving, and removing entries and managing groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lstpsche](https://clawhub.ai/user/lstpsche)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to keep a local, per-workspace todo list with groups and task statuses while keeping replies concise and avoiding separate todo files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and modifies a local SQLite todo.db in each workspace.

Mitigation: Install it only where that local database behavior is acceptable, and set TODO_DB deliberately when using a non-default location.

Risk: Remove, clear, and group remove --delete-entries can delete todo entries from the local database.

Mitigation: Confirm destructive targets before execution, and use the default group removal behavior unless the user explicitly asks to delete entries.

## Reference(s):

- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/lstpsche/skills/todo-management)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text confirmations and CLI output, with shell commands for todo operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sqlite3 and stores persistent state in a per-workspace todo.db unless TODO_DB overrides the location.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
