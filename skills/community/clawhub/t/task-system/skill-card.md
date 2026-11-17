## Description:

Task System manages local task lifecycles with SQLite tracking, task creation, heartbeat updates, completion status, stuck-task detection, and status summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npmisantosh](https://clawhub.ai/user/npmisantosh)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to create, update, complete, and review locally stored task records during agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently changes shell startup files and may alter PATH behavior.

Mitigation: Review the installer before use, prefer explicit opt-in PATH changes, and avoid writing to ~/.bashrc by default.

Risk: Task mutation commands can default to task ID 1 and do not validate task IDs before SQLite updates.

Mitigation: Require explicit task IDs, validate IDs as integers, and review updates before running mutations against the local database.

Risk: Unsafe task ID handling can corrupt or alter the local task database.

Mitigation: Back up the SQLite database and use parameterized or validated updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/npmisantosh/skills/task-system)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local task records in a SQLite database under the user's home directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
