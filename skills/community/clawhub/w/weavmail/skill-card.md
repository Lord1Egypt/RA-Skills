## Description:

Use weavmail CLI to manage emails for the current task. Use when you need to read, send, reply to, or move emails as part of completing a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yankeguo](https://clawhub.ai/user/yankeguo)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to configure the weavmail CLI, sync inbox messages into local Markdown files, and send, reply to, archive, trash, or move email as part of a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real email credentials.

Mitigation: Use app-specific passwords or OAuth where possible, and avoid putting passwords directly in chat or shell commands.

Risk: The skill can send or modify email, including archive, trash, move, and reply operations.

Mitigation: Require explicit final confirmation before sending, archiving, trashing, or moving any email.

Risk: Syncing without an account argument can operate across all configured accounts.

Mitigation: Restrict commands to a named account when the task should not apply to every configured account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yankeguo/skills/weavmail)
- [Publisher profile](https://clawhub.ai/user/yankeguo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and local email files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the uv binary and a configured email account; synced emails are represented as local Markdown files.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
