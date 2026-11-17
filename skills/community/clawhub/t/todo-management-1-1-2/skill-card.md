## Description:

Per-workspace SQLite todo manager (./todo.db) with groups and task statuses (pending/in_progress/done/skipped), operated via {baseDir}/scripts/todo.sh for adding, listing, editing, moving, and removing entries and managing groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucky-2968](https://clawhub.ai/user/lucky-2968)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to maintain a local, per-workspace todo list with groups and task statuses through a deterministic SQLite-backed CLI. It is intended for concise task capture, listing, updates, moves, and cleanup without creating markdown todo files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or changes a local todo.db in each workspace where it is used.

Mitigation: Install and use it only in workspaces where local todo database state is acceptable; set TODO_DB when a different database location is needed.

Risk: Using group remove with --delete-entries permanently deletes todo records in that group.

Mitigation: Use the default group removal behavior to move entries to Inbox unless the user explicitly confirms deletion.

Risk: Unused npm package files may cause dependency hygiene confusion for Node-based installation workflows.

Mitigation: Review the package files before publishing or installing through Node tooling and remove them if they are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucky-2968/skills/todo-management-1-1-2)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Concise text responses with occasional CLI output when the user explicitly requests todo lists or ambiguity resolution requires IDs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sqlite3 and may create or update a local todo.db in the active workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
