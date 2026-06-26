## Description: <br>
Track local todo or work-report items in a SQLite database, including planned work, progress amounts, completion status, deletion, and archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanmwx](https://clawhub.ai/user/seanmwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist todo and work-report state locally, update progress, list current work, summarize completion, archive history, and delete tasks only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains a persistent local todo database in the user's home directory. <br>
Mitigation: Install only when persistent local task storage is acceptable, and use TODO_LIST_DB_PATH for test isolation or explicit custom storage locations. <br>
Risk: Permanent deletion removes task rows from SQLite and future summaries. <br>
Mitigation: Prefer archiving for retained history and require explicit user confirmation before running delete commands. <br>


## Reference(s): <br>
- [TODO List Pro on ClawHub](https://clawhub.ai/seanmwx/todo-list-pro) <br>
- [Command Reference](artifact/references/commands.md) <br>
- [Natural-Language Reference](artifact/references/chat_reference.md) <br>
- [Storage Model](artifact/references/storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database at ~/.work_report_summary/todo_list.db by default; TODO_LIST_DB_PATH can override the path for tests or explicit custom setups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
