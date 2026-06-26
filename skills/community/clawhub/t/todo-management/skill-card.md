## Description: <br>
Per-workspace SQLite todo manager for adding, listing, editing, moving, removing, and grouping todo entries through a bundled CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lstpsche](https://clawhub.ai/user/lstpsche) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to manage a local project todo list in a per-workspace SQLite database while keeping agent responses concise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and modifies a local todo.db file in the active workspace. <br>
Mitigation: Install and use it only in workspaces where local todo storage is acceptable, or set TODO_DB to an intended database path. <br>
Risk: Todo entries may expose secrets or sensitive personal data if users store them in shared projects. <br>
Mitigation: Do not place secrets or sensitive personal data in todo entries, especially in shared repositories or collaborative workspaces. <br>
Risk: Clear, remove, and group deletion operations can delete todo data. <br>
Mitigation: Use explicit IDs for destructive changes and rely on the documented prompt flow before deleting group entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lstpsche/todo-management) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Short natural-language confirmations, todo-list text when requested, and bash CLI commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires sqlite3; stores tasks in ./todo.db by default unless TODO_DB is set.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
