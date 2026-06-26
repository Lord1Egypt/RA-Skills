## Description: <br>
微博全场景数据查询助手，整合 App、Web 和 V2 API，覆盖微博详情、用户数据、AI 搜索、高级搜索、热搜榜单、评论和视频数据查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, media teams, brand teams, and developers use this skill to query Weibo posts, users, search results, trending topics, comments, videos, and related engagement data for public-opinion monitoring and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, Weibo queries, and any supplied platform session cookies are sent to a third-party service. <br>
Mitigation: Use scoped credentials where available, avoid sharing platform cookies unless necessary, rotate credentials after use, and install only if the user accepts sending requests to aconfig.cn. <br>
Risk: The artifact includes unrelated Douyin/Xiaohongshu fallback instructions that may confuse routing or review. <br>
Mitigation: Review or remove those unrelated fallback instructions before deployment. <br>
Risk: Broad user, profile, follower, and social-graph endpoints can expose sensitive analysis patterns. <br>
Mitigation: Use these endpoints only for legitimate analysis with consent or another appropriate basis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/new-ironman/weibo-aggregate-scraper) <br>
- [MaxHub Website](https://www.aconfig.cn) <br>
- [Post & Comment API](references/api-post.md) <br>
- [User Data API](references/api-user.md) <br>
- [Search API](references/api-search.md) <br>
- [Trending & Hot API](references/api-trending.md) <br>
- [Video & Feed API](references/api-video-feed.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, tables, setup guidance, and curl-based API call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should match the user's language and avoid exposing API key values.] <br>

## Skill Version(s): <br>
3.6.1 (source: server evidence, frontmatter metadata, and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
