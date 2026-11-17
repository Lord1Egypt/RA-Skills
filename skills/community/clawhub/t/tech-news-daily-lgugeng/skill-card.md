## Description:

每日科技资讯聚合。自动抓取GitHub Trending、51CTO、百度热搜科技榜，筛选AI/Cloud/ML领域内容，生成结构化简报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and teams that use OpenClaw can generate scheduled Chinese-language technology news briefings from configured sources, with optional Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic delivery and hard-coded Feishu target metadata may send generated briefings to an unintended recipient.

Mitigation: Review and edit config.json before installation, especially push_target user_id and webhook settings.

Risk: The skill includes broad triggers and scheduled execution behavior.

Mitigation: Install only when a scheduled Chinese-language tech-news workflow is intended, and verify whether cron-config.json is honored automatically in the target environment.

Risk: Generated briefings may be misleading if source fetching or AI/Cloud/ML filtering does not match the skill claims.

Mitigation: Treat generated briefings as unverified drafts until source-fetching and filtering behavior has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgugeng/skills/tech-news-daily-lgugeng)
- [Publisher profile](https://clawhub.ai/user/lgugeng)
- [GitHub Search API](https://api.github.com/search/repositories)
- [Baidu technology hot list](https://top.baidu.com/board?tab=science)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown briefings and JSON report files, with optional Feishu card messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language daily briefing workflow; configured for up to 15 articles and optional scheduled delivery.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
