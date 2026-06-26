## Description: <br>
Todo Manager helps agents manage task lists, priorities, reminders, categories, and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to organize todo items, track status, set priority and due-date metadata, and request reminders through a ClawHub todo workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact metadata lists curl, but the skill documentation does not explain why network-capable tooling is required. <br>
Mitigation: Review the installed skill before use and only grant network-capable tools when the workflow actually requires them. <br>
Risk: Todo status, due dates, and reminders can become stale or incomplete if the user does not maintain the task data. <br>
Mitigation: Treat the skill output as task-management assistance and verify important deadlines or completion status before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/xiaoming-todo-manager) <br>
- [Publisher profile](https://clawhub.ai/user/kaising-openclaw1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and task-management guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe list, board, or calendar views for todo data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
