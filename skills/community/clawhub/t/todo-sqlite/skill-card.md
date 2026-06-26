## Description: <br>
Manage multi-project todos with SQLite, supporting subtasks, priority and urgency levels, keyword search, time filters, smart sorting, and scheduled reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LaoYutang](https://clawhub.ai/user/LaoYutang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage persistent local todo lists across projects, including subtasks, due dates, notes, status changes, search, and summary statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo titles, notes, project names, due dates, and completion history are stored in a persistent local SQLite database. <br>
Mitigation: Do not store secrets or sensitive personal data in todos, and handle the local database according to the user's data retention needs. <br>
Risk: Delete commands remove todos, child todos, or whole projects without built-in confirmation or undo. <br>
Mitigation: Review project names and todo IDs before deletion, and keep backups when the todo database is operationally important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LaoYutang/todo-sqlite) <br>
- [Publisher profile](https://clawhub.ai/user/LaoYutang) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal-oriented text and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a persistent local SQLite database at ~/.openclaw/workspace/data/todo.db.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
