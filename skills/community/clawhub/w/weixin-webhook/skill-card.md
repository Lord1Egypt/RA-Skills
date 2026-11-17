## Description:

Sends WeCom text or Markdown webhook notifications, including optional user or mobile mentions, for reminders and scheduled team updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiekch](https://clawhub.ai/user/xiekch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send WeCom group reminders from an agent, shell command, or scheduled OpenClaw cron task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook keys may be exposed through shell history, cron definitions, logs, or shared command text.

Mitigation: Store webhook keys in a protected secret file or secret manager, avoid pasting real keys into persistent commands, and rotate any key that may have been exposed.

Risk: Message content and mentions are sent to WeCom through the configured webhook.

Mitigation: Send only content appropriate for the target WeCom group and verify recipients before scheduling repeated notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiekch/skills/weixin-webhook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and webhook payload formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeCom webhook requests through curl; users supply the webhook key, message type, content, and optional mention lists.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
