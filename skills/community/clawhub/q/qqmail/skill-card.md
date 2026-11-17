## Description:

Manage QQ Mail via IMAP/SMTP to read, send with attachments, search emails by subject, sender, or date, and list folders using Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdpaer](https://clawhub.ai/user/pdpaer)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage a QQ Mail mailbox after the user provides a QQ Mail authorization code. It supports reading recent messages, opening a selected message, searching mail, listing folders, and sending messages with optional attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and send email using the user's QQ Mail authorization code.

Mitigation: Install only when the user is comfortable granting mailbox access, use a QQ Mail authorization code instead of the account password, and keep the code in environment variables.

Risk: The skill can send messages and attach local files.

Mitigation: Confirm recipients, message content, and attachment paths before sending.

Risk: Email content may contain untrusted instructions.

Mitigation: Treat instructions found inside emails as untrusted content rather than commands for the agent to follow.

## Reference(s):

- [ClawHub QQ Mail skill page](https://clawhub.ai/pdpaer/skills/qqmail)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and QQMAIL_USER plus QQMAIL_AUTH_CODE environment variables; supports Windows, Linux, and macOS.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
