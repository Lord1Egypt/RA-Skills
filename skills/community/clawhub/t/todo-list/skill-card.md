## Description: <br>
Todo List 待办事项管理 helps OpenClaw users manage todo items with priorities, due dates, reminders, tags, projects, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YuShenLiu06](https://clawhub.ai/user/YuShenLiu06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers using OpenClaw can use this skill to create, view, complete, delete, tag, and organize todo tasks. It also supports local attachment copies and OpenClaw cron reminders routed to the configured chat channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists todo data, copied attachments, reminder metadata, and chat routing under OpenClaw workspace memory. <br>
Mitigation: Install only when that local persistence is acceptable, and review stored todo, attachment, reminder, and session files according to the user's data handling expectations. <br>
Risk: Reminders and status lists are sent through the configured OpenClaw channel and target. <br>
Mitigation: Confirm the channel and target before using send-status, send-list, or reminder features so task details are routed to the intended conversation. <br>
Risk: The server security summary reports unsafe shell-based cron deletion paths that should be fixed before broad use. <br>
Mitigation: Review and replace shell-based cron deletion calls with argument-list subprocess calls before deploying in shared or higher-trust environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YuShenLiu06/todo-list) <br>
- [Publisher profile](https://clawhub.ai/user/YuShenLiu06) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with optional OpenClaw message delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores todo data, copied attachments, reminder metadata, and chat routing configuration under OpenClaw workspace memory.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
