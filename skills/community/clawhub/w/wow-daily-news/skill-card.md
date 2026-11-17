## Description:

每日日报自动生成。每天 18:00 自动生成包含魔兽世界新闻、NGA 热帖、今日美图的飞书文档，并推送到飞书和微信。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorexxar](https://clawhub.ai/user/lorexxar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to generate a scheduled World of Warcraft daily report that combines official and community news, selected forum discussions, image content, and Feishu/WeChat delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create external documents and send links to fixed Feishu and WeChat recipients.

Mitigation: Run only in a trusted environment, make recipients configurable, and require explicit confirmation before sending.

Risk: The skill can run unverified local scripts and a native binary and can start a background local service.

Mitigation: Bundle or pin dependencies and review executable paths before routine use.

Risk: The security scan identifies command-injection-prone shell execution.

Mitigation: Fix shell=True command execution before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorexxar/skills/wow-daily-news)
- [EXWIND World of Warcraft news source](https://exwind.net/)
- [Blizzard China World of Warcraft news](https://wow.blizzard.cn/news/)
- [NGA forum thread source](https://nga.178.com/read.php?tid=xxx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, API Calls, Guidance]

**Output Format:** [Lark-flavored Markdown report with links, image tags, delivery messages, and optional local markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Feishu documents, send Feishu and WeChat notifications, fetch external web content, and save generated report assets in the OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
