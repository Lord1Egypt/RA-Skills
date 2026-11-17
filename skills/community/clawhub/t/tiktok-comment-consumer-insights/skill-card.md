## Description:

从 TikTok 公开搜索结果、博主作品和视频评论中提取结构化数据，帮助归纳用户反馈、购买顾虑、内容表现与舆情。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

TikTok 创作者、品牌与市场团队可用它检索公开视频、查看博主作品并汇总视频评论，从而整理选题线索、竞品内容表现和用户反馈。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and TikTok links are sent to GUAIKEI to retrieve public TikTok data.

Mitigation: Use only public TikTok content and avoid submitting confidential, personal, or otherwise sensitive information in queries.

Risk: Security analysis was partial, and the scanner notes that the skill’s runtime permissions are not established by the scan.

Mitigation: Review the partially inspected components and confirm the external API access and token use before installation.

## Reference(s):

- [GUAIKEI 产品与访问令牌](https://www.guaikei.com)
- [命令参数参考](artifact/references/options.md)
- [更新日志](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data for TikTok search results, creator posts, or video comments; an agent can summarize it as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty or omit unavailable fields. Search and creator-post requests support up to 30 items per monthly token; comment requests support up to 40.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
