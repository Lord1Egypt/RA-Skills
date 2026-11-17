## Description:

QQ邮箱工作邮件监控与标注已读。当用户提到工作邮件通知、邮件日报、新邮件提醒、或需要标注邮件已读时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjiongjie](https://clawhub.ai/user/zhangjiongjie)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and mailbox operators use this skill to monitor QQ work-email folders, receive grouped new-mail notifications, inspect recent message bodies, and mark selected messages as read by notification index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access configured QQ work-email metadata and message bodies.

Mitigation: Install only for users and machines authorized to access that mailbox, and review message-body requests before execution.

Risk: The skill can mark mailbox items as read when invoked.

Mitigation: Confirm requested message indexes before running read-marking commands, especially in shared or delegated mailbox workflows.

Risk: Recent sender, subject, folder, and timestamp metadata are persisted locally.

Mitigation: Use only where local persistence under the OpenClaw workspace data directory is acceptable for work-email metadata.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with shell command examples and numbered email notification entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recent email sender, subject, folder, timestamp, message body text, and read-marking status.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
