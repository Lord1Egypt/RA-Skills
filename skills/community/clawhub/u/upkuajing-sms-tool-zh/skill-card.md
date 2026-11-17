## Description:

对接全球通信运营商发送批量跨境短信，实时查看每条短信的发送状态，助力外贸从业者开展海外营销推广、订单物流通知以及客户精细化触达。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External business users, marketers, sales teams, operations teams, and customer support teams use this skill to send international SMS messages, monitor task status, and review delivery records for cross-border commerce, logistics notifications, customer outreach, and reactivation campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles recipient phone numbers, SMS content, delivery records, and API keys.

Mitigation: Install only when the Upkuajing service is trusted with this data, avoid printing credential files or passing real API keys on the command line, and restrict local credential file permissions.

Risk: SMS sending and recharge flows can create paid account activity.

Mitigation: Require a separate explicit confirmation before each paid SMS send or recharge flow, and check current pricing before sending.

Risk: Bulk international messaging can create compliance, consent, and deliverability obligations.

Mitigation: Use the skill only for recipient lists and message content that have been reviewed for applicable consent, marketing, and local telecommunications requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/upkuajing-sms-tool-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing OpenAPI price information](https://www.upkuajing.com/web/openapi/price.html)
- [短信发送 API 参考](references/sms-send-api.md)
- [短信任务列表 API 参考](references/sms-task-list-api.md)
- [短信任务明细列表 API 参考](references/sms-task-record-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown guidance with Python command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read a local UPKUAJING_API_KEY credential file and may trigger paid SMS or recharge operations after explicit user confirmation.]

## Skill Version(s):

1.0.4 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
