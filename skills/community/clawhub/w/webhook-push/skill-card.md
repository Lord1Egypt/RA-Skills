## Description:

Webhook Push sends user-directed messages to WeChat Work, DingTalk, and Feishu group bots through configured webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysjyga](https://clawhub.ai/user/ysjyga)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers use this skill to send announcements, reminders, test messages, images, and simple Markdown content to configured enterprise chat groups from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook keys can authorize posts to configured enterprise chat groups if webhook-config.json is exposed.

Mitigation: Keep webhook-config.json private, store only required webhook keys, and avoid committing or uploading it.

Risk: A message may disclose secrets, personal data, or notify a broad audience through @all, phone, or user-ID mentions.

Mitigation: Confirm the recipient group, message content, and all mention targets before sending.

Risk: Platform rate limits, content limits, or sensitive-word filters may reject or throttle messages.

Mitigation: Throttle sends and shorten or split content according to each platform's documented limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ysjyga/skills/webhook-push)
- [WeChat Work group robot webhook endpoint](https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key})
- [DingTalk custom robot webhook endpoint](https://oapi.dingtalk.com/robot/send?access_token={key})
- [Feishu bot webhook endpoint](https://open.feishu.cn/open-apis/bot/v2/hook/{key})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown or text with Python examples, shell commands, and webhook request results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided webhook-config.json and sends outbound webhook requests to the selected chat platform.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
