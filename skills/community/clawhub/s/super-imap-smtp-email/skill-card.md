## Description:

Read, search, and manage email over IMAP and send email over SMTP, including multi-account support and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure standard IMAP/SMTP email accounts, inspect mailboxes, retrieve messages and attachments, mark messages, and send email from configured accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill receives direct access to configured email accounts and can read, modify, and send email.

Mitigation: Install only for accounts intended for agent access, use provider app passwords or authorization codes where available, and rotate credentials if the skill is removed or reconfigured.

Risk: The security evidence reports weak file access safeguards around selected local directories.

Mitigation: Keep allowed read and write directories narrow, avoid shared or symlinked locations, and review attachment paths before use.

Risk: The security evidence flags setup and temporary credential handling as requiring careful review.

Mitigation: Review the setup script before entering credentials and prefer a release that addresses the path-validation and temporary-credential issues.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/subaru0573/skills/super-imap-smtp-email)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Command-line text with mailbox data, message content, status messages, and downloaded attachment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured IMAP/SMTP credentials and optional allowlisted local directories for file reads and attachment downloads.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
