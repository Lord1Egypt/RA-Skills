## Description:

微博全场景数据查询助手，整合 App/Web/V2 多版本 API，覆盖微博详情、用户数据、AI 搜索、高级搜索、热搜榜单、评论和视频等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query read-only Weibo post, user, search, trending, comment, and video data through the MaxHub API for public opinion monitoring, brand tracking, media research, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends MaxHub API credentials and Weibo queries to aconfig.cn.

Mitigation: Use only when comfortable sharing those requests with the MaxHub service, avoid browser cookies unless necessary, prefer scoped tokens or test accounts, and rotate or revoke cookies after use.

Risk: The security review notes that failed requests can route to unrelated Douyin or Xiaohongshu-style API paths.

Mitigation: Review and remove or disable unrelated fallback material before deployment, and confirm request paths against the Weibo reference files before execution.

Risk: The release security verdict is suspicious and requires review before installation.

Mitigation: Review the skill before installing and prefer a pinned or already verified ClawHub CLI installation.

## Reference(s):

- [Post and Comment API](references/api-post.md)
- [Search API](references/api-search.md)
- [Trending API](references/api-trending.md)
- [User API](references/api-user.md)
- [Video and Feed API](references/api-video-feed.md)
- [Parameter Mappings](references/param-mappings.md)
- [MaxHub API Service](https://www.aconfig.cn)
- [ClawHub Skill Listing](https://clawhub.ai/new-ironman/skills/weibo-aggregate-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; outputs should omit secret values.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
