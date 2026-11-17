## Description:

从 TikTok 公开数据中搜索内容与创作者、查看作品及评论，并返回结构化 JSON，支持达人筛选和内容分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

TikTok creators, agencies, brands, and research teams use the skill to find public creators and content, review post engagement and comments, and support influencer, competitor, and content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security verdict has medium confidence: only 20 of 32 components were fully inspected and the tool-misuse analyzer was degraded.

Mitigation: Treat the verdict as limited; review the declared scope and fixed timestamp setting before installation.

Risk: Queries send keywords or TikTok links to the Guaikei service.

Mitigation: Use only query data you are comfortable sharing with that provider, and review its terms and privacy practices.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/tiktok-kol-discovery)
- [Guaikei service and API access](https://www.guaikei.com)
- [Usage options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON envelope containing search, creator-post, or comment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields vary by command; result counts depend on the query and API plan.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
