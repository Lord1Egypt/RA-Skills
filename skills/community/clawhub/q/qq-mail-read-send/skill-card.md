## Description:

Reads and sends QQ Mail messages using IMAP for mailbox access and SMTP for outbound email, with guidance for authorization-code credentials and multi-encoding message parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent inspect recent QQ Mail messages, search or filter mailbox content, and send simple text emails through QQ Mail after credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles QQ Mail credentials and mailbox access.

Mitigation: Use a dedicated QQ Mail authorization code, store it with owner-only permissions, and never commit or share the credential file.

Risk: Outbound email sending can disclose information or send unintended messages.

Mitigation: Require explicit user confirmation before sending and verify recipients, subject, body, cc, and bcc before SMTP submission.

Risk: The artifact shows inconsistent credential paths between the documentation and Python sender module.

Mitigation: Verify the active credential path before use and align the script configuration with the documented secrets file.

Risk: Mailbox reads may expose private email content beyond the user's intended scope.

Mitigation: Confirm the requested mailbox scope and filters before reading, searching, summarizing, or displaying email content.

## Reference(s):

- [QQ Mail IMAP/SMTP Help](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)
- [Message Sending Reference](references/message-sending.md)
- [ClawHub Skill Page](https://clawhub.ai/openclawzhangchong/skills/qq-mail-read-send)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Text]

**Output Format:** [Markdown with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAIL_USER and MAIL_PASS credentials and may perform mailbox reads or outbound email sends when the agent follows the skill.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
