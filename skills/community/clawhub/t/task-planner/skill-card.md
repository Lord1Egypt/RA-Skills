## Description: <br>
Manage tasks, set priorities, and track deadlines locally with bilingual documentation and no cloud sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use Task Planner to maintain a local to-do list, assign priorities and due dates, list pending or completed work, and mark tasks done without cloud sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions, priorities, due dates, and completion status are stored locally in a JSON file and may contain sensitive user-entered details. <br>
Mitigation: Avoid storing secrets or highly sensitive personal details in task text, and use TASK_PLANNER_DIR to place task data in an appropriate local directory when isolation is needed. <br>


## Reference(s): <br>
- [Task Planner on ClawHub](https://clawhub.ai/xueyetianya/task-planner) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash examples and local JSON task data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task data in ~/.task-planner/tasks.json unless TASK_PLANNER_DIR is set.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
