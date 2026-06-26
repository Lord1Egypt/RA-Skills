## Description: <br>
Webhook Notify provides PowerShell helpers for sending templated webhook notifications to DingTalk, WeCom, Feishu, Slack, Discord, Telegram, and custom HTTP endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imzhulei](https://clawhub.ai/user/imzhulei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to add cross-platform webhook notifications, alert templates, batch sends, and connection checks to automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send outbound messages to user-supplied webhook URLs, including custom HTTP endpoints. <br>
Mitigation: Use only trusted webhook destinations, and avoid the custom HTTP helpers unless the destination and method are explicitly controlled. <br>
Risk: Webhook URLs often contain secret tokens. <br>
Mitigation: Store webhook URLs in environment variables or a secrets manager, and avoid placing them in prompts, logs, scripts, or shared configuration. <br>
Risk: Alert payloads may expose sensitive operational or customer data to third-party messaging platforms. <br>
Mitigation: Review notification content before sending and limit payloads to information approved for the target platform and audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imzhulei/webhook-notify) <br>
- [DingTalk custom bot documentation](https://open.dingtalk.com/document/orgapp/custom-bot-to-send-group-chat-messages) <br>
- [WeCom group robot documentation](https://developer.work.weixin.qq.com/document/path/91770) <br>
- [Feishu custom bot documentation](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN) <br>
- [Slack incoming webhooks](https://api.slack.com/messaging/webhooks) <br>
- [Discord webhooks](https://support.discord.com/hc/articles/228383668) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline PowerShell code blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PowerShell and sends outbound HTTP requests to user-supplied webhook URLs.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata; artifact package.json and VERSIONS.md report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
