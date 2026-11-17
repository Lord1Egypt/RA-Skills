## Description:

Manages QQ Enterprise Mail through IMAP/SMTP commands to list, read, search, send, reply, forward, mark messages, inspect folders, and report mailbox statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangmu-git2](https://clawhub.ai/user/liangmu-git2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a configured mailbox, including reading, searching, sending, replying, forwarding, marking mail, listing folders, and checking mailbox statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials are stored in a local plaintext configuration file.

Mitigation: Use a revocable app-specific password, restrict permissions on config/email-config.json, and avoid committing or sharing the configured directory.

Risk: The skill can send, reply, forward, reply-all, mark messages, and attach local files.

Mitigation: Require explicit user confirmation before any mailbox-changing action or attachment operation.

Risk: Connected mailboxes may contain sensitive personal, business, or regulated information.

Mitigation: Review messages and recipients before disclosure, and install the skill only for mailboxes appropriate for agent access.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON command output with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands run a local Python IMAP/SMTP client configured by config/email-config.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
