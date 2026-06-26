## Description: <br>
Use when managing todos, tasks, projects, or kanban boards via Taskleef.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xatter](https://clawhub.ai/user/Xatter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and task-management users use this skill to let an agent manage Taskleef todos, projects, subtasks, and kanban boards through the Taskleef CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to run downloaded Taskleef CLI code. <br>
Mitigation: Review the downloaded todo CLI before execution and install dependencies from trusted sources. <br>
Risk: The skill depends on TASKLEEF_API_KEY for account access. <br>
Mitigation: Keep TASKLEEF_API_KEY out of repositories and logs, and store it only in the intended agent or shell configuration. <br>
Risk: Delete, project delete, and board clear actions can remove or clear user data. <br>
Mitigation: Require explicit user confirmation before running destructive Taskleef commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xatter/taskleef) <br>
- [Publisher profile](https://clawhub.ai/user/Xatter) <br>
- [Taskleef website](https://taskleef.com) <br>
- [Taskleef CLI installer](https://raw.githubusercontent.com/Xatter/taskleef/main/taskleef-cli/todo) <br>
- [jq Linux x86_64 release](https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64) <br>
- [jq Linux arm64 release](https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-arm64) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that read, create, update, complete, delete, move, assign, or clear Taskleef items.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
