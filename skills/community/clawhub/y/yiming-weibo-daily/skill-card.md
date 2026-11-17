## Description:

张一鸣微博金句飞书私聊技能。安装后每小时推送一条张一鸣微博精选，附主题标签和今日练习。适用于安装、配置、试发和排查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocke1001feller](https://clawhub.ai/user/rocke1001feller)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, configure, preview, test-send, schedule, and troubleshoot hourly Feishu private-message delivery of selected Zhang Yiming Weibo quotes with topic tags and daily practice prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu credentials or unrelated environment variables could be reused beyond the user's intent.

Mitigation: Use only Feishu credentials intentionally provided for this skill; do not copy secrets from other skills or unrelated environment variables.

Risk: The skill can send live Feishu messages or enable hourly delivery without clear approval.

Mitigation: Ask before any real message is sent or hourly schedule is enabled, and preview message content before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rocke1001feller/skills/yiming-weibo-daily)
- [Project homepage](https://github.com/Rocke1001feller/yiming-weibo-daily)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and environment-variable names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preview generated message content, perform a real Feishu test send, and provide scheduling or troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and publish metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
