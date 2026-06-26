## Description: <br>
Manage tasks with persistent SQLite storage, including creation, retrieval, updates, deletion, filtering by status or priority, and status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makkzone](https://clawhub.ai/user/makkzone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to maintain a local persistent TODO list with task status, priority, timestamps, and CRUD operations from Python or the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task titles and descriptions are stored in a local SQLite database and may persist sensitive information. <br>
Mitigation: Do not store secrets or confidential data in task text; remove the local tasks.db file when stored task data should no longer persist. <br>
Risk: Delete commands remove tasks from the local database. <br>
Mitigation: Confirm task IDs before deleting important tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/makkzone/task-todo) <br>
- [Publisher profile](https://clawhub.ai/user/makkzone) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands] <br>
**Output Format:** [Structured Python dictionaries and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local tasks.db SQLite database in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
