## Description:

Set up periodic monitoring for IMAP mailboxes, guide mailbox configuration, test connectivity, and schedule recurring checks that summarize new messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiusuo9809](https://clawhub.ai/user/qiusuo9809)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure scheduled monitoring for Gmail, Outlook/Hotmail, QQ, Yahoo, 163/126, or generic IMAP mailboxes and receive concise or summarized notifications for new messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials are stored in a local plaintext config file and allow ongoing access to email content.

Mitigation: Use only app-specific passwords where available, protect or remove the local config when no longer needed, and avoid primary account passwords.

Risk: If attachment downloading is enabled, sender-controlled attachment filenames may be written to disk.

Mitigation: Keep attachment downloading disabled unless filename handling is fixed; if enabled, use a dedicated directory and treat downloaded files as untrusted.

## Reference(s):

- [IMAP Setup Reference](references/imap-setup.md)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration; the fetch script prints JSON arrays of new email summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration and state files, schedule a cron task, and optionally write email attachments to a user-selected directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
