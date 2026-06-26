## Description: <br>
Manage tasks with automatic creation, SQLite tracking, heartbeat updates, notifications, stuck task detection, and recovery in a complete lifecycle system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npmisantosh](https://clawhub.ai/user/npmisantosh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create, update, complete, list, and recover local work tasks through a shell-based SQLite task tracker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer adds persistent command-line access by modifying shell PATH setup and may create a task-system symlink. <br>
Mitigation: Install only when persistent local CLI access is desired, and review or remove the added shell PATH entry and ~/.local/bin/task-system symlink when uninstalling. <br>
Risk: Task text and notes are stored in a local SQLite database and may persist sensitive information. <br>
Mitigation: Avoid putting secrets, credentials, or other sensitive material in task requests or completion notes. <br>
Risk: Task operations depend on caller-supplied task IDs and local shell scripts. <br>
Mitigation: Use numeric task IDs and review command arguments before running update, complete, or stuck-task checks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/npmisantosh/task-system) <br>
- [Publisher Profile](https://clawhub.ai/user/npmisantosh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local SQLite task records under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
