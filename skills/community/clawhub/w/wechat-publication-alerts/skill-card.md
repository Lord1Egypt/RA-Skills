## Description:

使用曼格云云端服务订阅公众号发文提醒，配置邮件、飞书、企业微信、钉钉或 Webhook，查询新文章、监听和送达状态，管理暂停、恢复与续费。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

公众号运营者和开发者用它订阅发文通知、配置接收渠道，并查看监听和投递状态或管理续费。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription changes may incur charges or enable automatic renewal.

Mitigation: Review the live quote, target accounts, notification channels, and total budget before approving a purchase; enable renewal only when requested.

Risk: Alert configuration uses an external service and an API credential.

Mitigation: Confirm use of Mangyun's API and store the key in a local environment variable rather than sharing it in chat.

Risk: A channel test or accepted delivery does not prove a new article was detected or read.

Mitigation: Check monitoring and delivery status separately, and investigate uncertain outcomes before retrying notifications or purchases.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dunkong/skills/wechat-publication-alerts)
- [命令与渠道](references/commands.md)
- [曼格云产品文档](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and JSON status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports quoted costs, subscription settings, monitoring status, and delivery status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
