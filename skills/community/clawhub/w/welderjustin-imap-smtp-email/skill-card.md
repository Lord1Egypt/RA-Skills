## Description:

Read and send email via IMAP/SMTP, including checking for new or unread messages, fetching content, searching mailboxes, marking messages as read or unread, and sending email with attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welderjustin](https://clawhub.ai/user/welderjustin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent inspect, search, and update mailboxes over IMAP and send messages over SMTP. It supports common mail providers and can send or retrieve attachments when local file access is explicitly configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox access and outbound mail capability can expose, modify, or send sensitive communications.

Mitigation: Install only when mailbox read/write and send access are acceptable; prefer app-specific passwords and keep the .env file private.

Risk: Messages and attachments can be sent to external recipients.

Mitigation: Review recipients, message content, and attachments before sending.

Risk: Attachment download and send operations interact with local files.

Mitigation: Restrict ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS to the narrowest required directories and avoid shared or symlink-prone paths.

Risk: TLS certificate validation can be disabled for some mail server configurations.

Mitigation: Keep certificate verification enabled unless a trusted private mail server requires a self-signed certificate exception.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/welderjustin/skills/welderjustin-imap-smtp-email)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, IMAP/SMTP credentials, and explicit local read/write directory allowlists for attachment operations.]

## Skill Version(s):

0.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
