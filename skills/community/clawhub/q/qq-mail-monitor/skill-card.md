## Description:

QQ Mail Monitor helps an agent check QQ Mail for new messages, report recent mailbox metadata, provide TTS-ready notification text, and send test email through a configured account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksswei](https://clawhub.ai/user/ksswei)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to monitor a QQ Mail inbox for new messages, create reminder workflows, retrieve recent message metadata, and send a test email from the configured account. It is suited to notification, verification-code, and mailbox automation workflows where the account owner has approved access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires QQ Mail credentials that can read inbox metadata and send mail through the configured account.

Mitigation: Use a dedicated low-sensitivity mailbox, move credentials out of source files into a secret store, and revoke any exposed authorization code before use.

Risk: Automated cron checks and TTS notifications may expose email subjects, senders, or verification-code-related metadata.

Mitigation: Confirm the polling schedule, notification channel, and TTS behavior before enabling monitoring, and avoid routing sensitive mailbox content to shared devices.

Risk: Mail-sending capability can send messages from the configured account.

Mitigation: Limit use to accounts approved for automation and review any send workflow before allowing it to run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ksswei/skills/qq-mail-monitor)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ksswei)
- [QQ Mail](https://mail.qq.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus plain-text and JSON/status-line script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include email subject, sender, date, mailbox counts, TTS-ready notification text, and local state-file updates.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
