## Description:

汇总 TikTok 公开搜索、博主作品和视频评论数据，并生成内容表现复盘与可验证的下一步策略。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

TikTok 创作者、营销团队和研究人员可用它查询公开视频、创作者作品及评论数据，再据此分析内容表现、竞品和受众反馈。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security inspection was incomplete, and the supplied guidance notes undeclared tool scope.

Mitigation: Consider the inspection limitation and review the skill's permissions before installing, especially when host permissions matter.

Risk: Search terms and TikTok links are sent to GUAIKEI's service to retrieve data.

Mitigation: Use only public TikTok queries whose disclosure to that service is acceptable.

## Reference(s):

- [GUAIKEI service and token access](https://www.guaikei.com)
- [CLI options](references/options.md)
- [Release changelog](references/changelog.md)
- [ClawHub release page](https://clawhub.ai/why20261/skills/tiktok-performance-review)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data for TikTok search results, creator posts, and video comments, suitable for analysis and content reviews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes public content and engagement fields; responses distinguish successful, empty, and error results.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
