## Description:

帮助分析小红书公开笔记、博主作品和评论，以比较品牌表现、追踪竞品动态并发现内容机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

品牌运营、市场研究和内容团队可按关键词或小红书公开链接获取笔记、博主作品、互动数据和评论，用于竞品对比、舆情洞察、选题和 KOL 筛选。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Xiaohongshu links are sent to the third-party guaikei.com service.

Mitigation: Use the skill only if that data sharing is acceptable; avoid sensitive search terms and links.

Risk: Public-content results remain in local temporary logs.

Mitigation: Avoid sensitive queries or outputs and manage local logs according to your retention policy.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/xiaohongshu-competitor-radar)
- [Project homepage listed in skill metadata](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Data provider and token information](https://www.guaikei.com)
- [Usage options](artifact/references/options.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Analysis]

**Output Format:** [Markdown summaries with structured public-data results and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GUAIKEI_API_TOKEN; query results are also saved in local temporary logs.]

## Skill Version(s):

1.1.4 (source: ClawHub release metadata, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
