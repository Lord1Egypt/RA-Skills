## Description:

Webhook Notify helps agents send templated notifications to DingTalk, WeCom, Feishu, Slack, Discord, Telegram, and custom webhook endpoints with platform detection and retry handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imzhulei](https://clawhub.ai/user/imzhulei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to let an agent prepare or run PowerShell-based webhook notifications for alerting, deployment updates, monitoring events, and batch messages across supported chat platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound webhook helpers can send agent-generated content to external services or unknown hosts.

Mitigation: Install only for workflows that require external notifications, and review the destination URL, payload, and HTTP method before use, especially for custom HTTP helper calls.

Risk: Webhook URLs are secrets and may allow unauthorized posting if exposed.

Mitigation: Treat webhook URLs as secrets, avoid logging or displaying them, and prefer a secret manager over persistent user environment variables.

## Reference(s):

- [Webhook Notify on ClawHub](https://clawhub.ai/imzhulei/skills/webhook-notify)
- [DingTalk Custom Bot Documentation](https://open.dingtalk.com/document/orgapp/custom-bot-to-send-group-chat-messages)
- [WeCom Group Robot Documentation](https://developer.work.weixin.qq.com/document/path/91770)
- [Feishu Bot Webhook Documentation](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Discord Webhooks](https://support.discord.com/hc/articles/228383668)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell code blocks, configuration notes, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute outbound HTTP POST requests when the generated PowerShell helper is run.]

## Skill Version(s):

2.0.2 (source: server release evidence; artifact package.json and VERSIONS.md list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
