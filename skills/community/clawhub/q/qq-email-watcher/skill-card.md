## Description:

Monitors new messages from whitelisted senders in a QQ Mail inbox and sends QQ notifications with AI summaries, key-detail highlighting, and concise previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhang-lxuan](https://clawhub.ai/user/zhang-lxuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QQ Mail users use this skill to configure a mailbox watcher that filters senders through a whitelist and forwards new-mail notifications to QQ. It is useful for reminders, verification-code alerts, and automated monitoring of selected contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports hardcoded mailbox credentials and a fixed QQ notification target, which could expose email data without clear user control.

Mitigation: Remove bundled credentials and target identifiers before use, revoke the included IMAP authorization code, and replace all account and recipient values with protected user-controlled configuration.

Risk: Email subjects and message previews may be sent to an AI summarization command and then forwarded to QQ.

Mitigation: Disable or constrain AI summarization for sensitive mailboxes and confirm that forwarding email content to QQ is acceptable for the mailbox owner.

Risk: Whitelist matching may not strictly limit notifications to the intended senders.

Mitigation: Review and fix whitelist matching logic before monitoring a real mailbox, and test notifications with controlled sender addresses.

## Reference(s):

- [QQ Mail Monitor Configuration Guide](references/configure.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces QQ notification text from watched email metadata and message previews.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
