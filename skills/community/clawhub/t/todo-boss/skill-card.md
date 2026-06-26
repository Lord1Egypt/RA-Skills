## Description: <br>
Capture and track tasks with owner and due date, mark done, list open or delegated tasks, and get daily reports via Telegram commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ukraecho](https://clawhub.ai/user/ukraecho) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to capture Telegram task requests, require owner and due date fields, track delegated work, and produce concise remaining-work reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted task text could cause unintended local Python execution or corrupt the task log. <br>
Mitigation: Fix the add-task script to pass task fields as data, such as argv, stdin, or environment variables with proper JSON serialization, before installation. <br>
Risk: Task contents are stored on disk in a local JSONL log. <br>
Mitigation: Use only in environments where local task persistence is acceptable and review the stored task data path before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ukraecho/todo-boss) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Concise Telegram-facing text with local shell command execution for task logging] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an append-only local JSONL task log under the user's home directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
