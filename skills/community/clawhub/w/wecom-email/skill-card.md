## Description:

企业微信邮箱操作 - 使用专用邮箱发送邮件，支持读取会议纪要、业务文档等作为邮件内容发送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to prepare and send work-related email through a dedicated WeCom mail account, including meeting minutes and business-document content. It is intended for explicit user-requested sends with confirmed recipients, subject, and message body.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses a mail-sending credential and can send workspace document content by email.

Mitigation: Use a narrowly scoped dedicated service account and require explicit confirmation of recipient, subject, and exact content before sending.

Risk: The evidence notes raw credential decoding and references personal mailbox secrets.

Mitigation: Do not store credentials with Base64, remove personal mailbox credential references, and review credential storage before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chongjie-ran/skills/wecom-email)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email content may include workspace document text and should be reviewed before sending.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
