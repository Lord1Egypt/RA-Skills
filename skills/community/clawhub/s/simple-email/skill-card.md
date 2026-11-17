## Description:

Simple Email lets an agent receive, search, read, mark, and download mail over IMAP and send plain text, HTML, and attachment email over SMTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiming-git](https://clawhub.ai/user/shiming-git)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can configure an email account so an agent can inspect mailbox contents, search or update message state, download attachments, and send outbound email through standard IMAP and SMTP providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured account gives the skill authority to read mailbox contents and send email.

Mitigation: Use an app password or authorization code for an account intended for agent use, and install only where that mailbox access is acceptable.

Risk: Downloaded attachments can overwrite files in the allowed download folder.

Mitigation: Use a narrow, dedicated ALLOWED_WRITE_DIRS location and review attachment names before downloading.

Risk: Broad read and write allowlists can expose workspace files to outgoing attachments or incoming downloads.

Mitigation: Set ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS to dedicated folders instead of the OpenClaw workspace.

Risk: Disabling certificate verification can weaken protection for mail server connections.

Mitigation: Keep certificate verification enabled unless you control the mail server and understand the trust boundary.

## Reference(s):

- [Simple Email on ClawHub](https://clawhub.ai/shiming-git/skills/simple-email)
- [OpenClaw skills homepage](https://github.com/openclaw/skills)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell command examples; CLI tools return JSON and may create downloaded attachment files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, IMAP and SMTP credentials, and configured read/write directory allowlists.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
