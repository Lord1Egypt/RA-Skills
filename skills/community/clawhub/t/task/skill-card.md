## Description: <br>
Tasker docstore task management via tool-dispatch. Use for task lists, due today/overdue, week planning, add/move/complete, or explicit /task commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amirbrooks](https://clawhub.ai/user/amirbrooks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Tasker-backed task lists from natural language or explicit /task commands, including listing, adding, completing, capturing, and viewing tasks by project or week. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered /task content is forwarded unchanged to the tasker_cmd tool. <br>
Mitigation: Use the skill only with a trusted tasker_cmd tool and avoid entering sensitive text unless the downstream tool's handling is acceptable. <br>
Risk: Task changes may affect a user's task store through add, complete, capture, note, board, and configuration commands. <br>
Mitigation: Review command intent before execution and prefer selector resolution for ambiguous task references. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amirbrooks/task) <br>
- [Publisher profile](https://clawhub.ai/user/amirbrooks) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown and tasker command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses human-readable output by default and can request Telegram/WhatsApp-friendly formatting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
