## Description:

Send and receive emails via QQ Mail SMTP/IMAP for inbox checks, message reading, document sharing, and notifications after configuring a QQ Mail authorization code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chao-nj-cn](https://clawhub.ai/user/chao-nj-cn)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent send QQ Mail messages, list inbox items, read specific emails, save attachments, and mark messages as read. It is intended for configured QQ Mail accounts where the user has explicitly provided authorization credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires QQ Mail credentials that allow sending and reading mailbox content.

Mitigation: Install only for accounts where this access is acceptable, prefer environment or scoped secret storage over TOOLS.md, and revoke the QQ authorization code if exposure is suspected.

Risk: The --save path can write attachments from email messages to disk.

Mitigation: Avoid saving attachments from untrusted emails until filenames are sanitized and overwrite protection is added; use a controlled output directory when saving is necessary.

## Reference(s):

- [QQ Mail](https://mail.qq.com)
- [ClawHub skill page](https://clawhub.ai/chao-nj-cn/skills/qq-email)
- [Publisher profile](https://clawhub.ai/user/chao-nj-cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI responses are text by default and JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send email, read mailbox content, mark messages as read, and save attachments when invoked with configured QQ Mail credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
