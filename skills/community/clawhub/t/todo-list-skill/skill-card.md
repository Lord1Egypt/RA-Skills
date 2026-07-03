## Description: <br>
Maintains a personal cross-session TODO list from natural-language requests, with SQLite persistence, priorities, tags, CLI commands, and optional WorkBuddy or DingTalk reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenqing24](https://clawhub.ai/user/chenqing24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to add, list, update, complete, and delete personal tasks from conversational requests or CLI commands. It is intended for single-user task tracking with local history, audit logging, and optional scheduled reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task records and audit history may retain exact user wording, including sensitive personal or financial details. <br>
Mitigation: Avoid putting secrets or highly sensitive details in tasks, review local retention behavior, and back up the database before uninstalling or cleanup. <br>
Risk: Reminder features can create scheduled jobs through WorkBuddy or cron-like automation. <br>
Mitigation: Choose the reminder channel explicitly and inspect created automations before relying on or leaving them enabled. <br>
Risk: DingTalk notifications may send task details outside the local workspace. <br>
Mitigation: Use DingTalk only for task content appropriate for that channel and disable or reconfigure external notification paths when not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenqing24/todo-list-skill) <br>
- [Command reference](references/commands.md) <br>
- [Trigger reference](references/triggers.md) <br>
- [Error handling and fallback paths](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance with CLI examples, status messages, and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite task data, local configuration, fallback files, and scheduled reminder jobs when enabled.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata, artifact changelog, pyproject.toml, manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
