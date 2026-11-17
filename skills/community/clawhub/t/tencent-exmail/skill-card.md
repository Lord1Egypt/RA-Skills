## Description:

Tencent Exmail skill for sending, reading, searching, downloading attachments, moving messages, and monitoring new mail through IMAP/SMTP over SSL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nopassword2000](https://clawhub.ai/user/nopassword2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent work with a Tencent Enterprise Mail account, including composing messages, reading inbox content, searching folders, downloading attachments, and watching for new mail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, send, mark, move, and monitor email in the connected Tencent Exmail account.

Mitigation: Use an account appropriate for agent access, review send and move actions before execution, and confirm mailbox changes match user intent.

Risk: Mailbox credentials are required through EXMAIL_ADDRESS and EXMAIL_PASSWORD.

Mitigation: Prefer an app-specific authorization code and keep credentials out of logs, shared files, and source control.

Risk: Downloaded attachments and hook-file records may contain private mailbox data.

Mitigation: Write attachments and hook files only to private directories that the user controls, and clean them up when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nopassword2000/skills/tencent-exmail)
- [Publisher profile](https://clawhub.ai/user/nopassword2000)
- [Tencent Exmail](https://exmail.qq.com)
- [Tencent Exmail help](https://exmail.qq.com/help)
- [Server configuration reference](references/server-config.md)
- [Troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, terminal text, and optional JSON hook-file records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the imapclient package for IMAP IDLE monitoring, and EXMAIL_ADDRESS plus EXMAIL_PASSWORD environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
