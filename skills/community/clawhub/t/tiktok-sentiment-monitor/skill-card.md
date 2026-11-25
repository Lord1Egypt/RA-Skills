## Description:

按关键词、创作者主页或视频链接检索 TikTok 公开视频与评论，并返回结构化数据供舆情、选题和竞品分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌团队和研究人员可用它查找 TikTok 公开视频、博主作品与评论，再整理舆情、选题和竞品口碑分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms or TikTok links are sent to an external service, and timestamps use Beijing time.

Mitigation: Use only search terms and public links you are comfortable sharing with that service, and account for Beijing time when interpreting events.

Risk: Security inspection was partial: 20 of 32 components were fully scanned and 12 were only partially inspected, resulting in medium confidence.

Mitigation: Review the skill and the service's data handling before installing, as recommended by the security assessment.

## Reference(s):

- [Usage options](references/options.md)
- [Changelog](references/changelog.md)
- [ClawHub release page](https://clawhub.ai/why20261/skills/tiktok-sentiment-monitor)
- [TikTok定向舆情监测助手官网](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured JSON data for agent analysis and concise text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public TikTok search, creator post, or comment data; some fields may be absent and media links may expire.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
