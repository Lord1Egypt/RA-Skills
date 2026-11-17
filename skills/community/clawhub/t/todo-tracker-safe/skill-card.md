## Description:

Secure TODO tracker with input validation and safe file operations. Use for task management across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gothicfox](https://clawhub.ai/user/gothicfox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a session-persistent TODO list, organize tasks by priority, mark tasks complete, remove tasks, and show concise status summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports suspicious file handling when shared workspaces or a manually set TODO_FILE are used.

Mitigation: Review before installing in shared workspaces, prefer the default private OpenClaw workspace path, and avoid group- or world-writable directories.

Risk: The TODO file path, symlink, and temporary-file handling are not described as hardened for multi-user use.

Mitigation: Do not rely on this skill as a hardened multi-user TODO store until those file-handling concerns are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gothicfox/skills/todo-tracker-safe)
- [Publisher Profile](https://clawhub.ai/user/gothicfox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Plain text command output and Markdown TODO file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bash, grep, awk, and sed; TODO_FILE can override the default TODO file path.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
