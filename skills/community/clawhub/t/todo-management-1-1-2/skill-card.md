## Description: <br>
Per-workspace SQLite todo manager (./todo.db) with groups and task statuses (pending/in_progress/done/skipped), operated via {baseDir}/scripts/todo.sh for adding, listing, editing, moving, and removing entries and managing groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lucky-2968](https://clawhub.ai/user/Lucky-2968) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage project-local todo items through a SQLite-backed CLI, including groups, statuses, listing, editing, moving, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo entries persist in todo.db and may expose sensitive information if secrets are stored as task text. <br>
Mitigation: Avoid storing secrets, credentials, or other sensitive material in todos. <br>
Risk: Clear, remove, and --delete-entries operations can permanently delete todo entries. <br>
Mitigation: Require an explicit user choice before destructive deletion and ask for an ID when the requested target is ambiguous. <br>
Risk: The artifact includes unused npm and pnpm package metadata unrelated to the SQLite todo workflow. <br>
Mitigation: Do not run npm or pnpm install in the skill folder unless the publisher explains why those package files are present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lucky-2968/todo-management-1-1-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Concise text responses and CLI-backed todo list output when explicitly requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses sqlite3 and persists todo data in a workspace-local todo.db file unless TODO_DB is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
