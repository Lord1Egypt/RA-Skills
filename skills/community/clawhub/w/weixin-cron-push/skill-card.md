## Description:

通过 OpenClaw Cron 定时任务向微信用户主动推送消息（天气、提醒、新闻摘要等），支持一次性 at、循环 cron/every 任务，并通过 sessionKey 路由到指定微信用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gausshj](https://clawhub.ai/user/gausshj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create scheduled WeChat reminders, daily pushes, and recurring notifications through the openclaw-weixin channel. It helps route automated messages to a specific WeChat user or account after a sessionKey has been established.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create scheduled and recurring WeChat messages to a selected sessionKey.

Mitigation: Review the recipient sessionKey, schedule, message content, account, and delete-after-run behavior before allowing task creation.

Risk: The skill describes local account and session files that may contain sensitive tokens or identifiers.

Mitigation: Do not expose ~/.openclaw account/session files or bearer tokens in prompts, logs, shared outputs, or screenshots.

Risk: The security review flags broad recurring-message behavior with limited user-control and privacy safeguards.

Mitigation: Prefer explicit user confirmation for recurring tasks and periodically audit active cron jobs with openclaw cron list.

Risk: Installer and plugin commands may pull external packages.

Mitigation: Use pinned or verified installer versions and review plugin provenance before enabling the WeChat channel.

## Reference(s):

- [Skill page](https://clawhub.ai/gausshj/skills/weixin-cron-push)
- [Weixin API reference](references/weixin-api.md)
- [WeChat plugin backend](https://ilinkai.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create one-time or recurring OpenClaw cron task proposals that send messages through WeChat when executed.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
