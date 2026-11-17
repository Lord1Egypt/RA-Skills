## Description:

西瓜视频数据查询助手。覆盖视频详情、用户数据、搜索、评论等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, analysts, and external users use this skill to query Xigua video, user, search, playback, and comment data through MaxHub APIs, then summarize or compare the results for content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xigua video IDs, user IDs, search terms, and comment lookup parameters to MaxHub/aconfig.cn using the configured API key.

Mitigation: Use only with data the user is comfortable sharing with MaxHub/aconfig.cn, keep MAXHUB_API_KEY secret, and avoid echoing credential values in responses or logs.

Risk: Failure handling can route some requests to unrelated Douyin endpoints, which may broaden data-sharing or produce results outside the intended Xigua scope.

Mitigation: Before deployment, remove or clearly separate unrelated Douyin and Xiaohongshu fallback references, and verify endpoint paths against the bundled Xigua reference files.

Risk: The scanner classified the release as suspicious because the data-sharing scope is under-disclosed.

Mitigation: Review the skill before installation and disclose the external API provider, request parameters, required API key, and network destination to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/xigua-aggregate-scraper)
- [Publisher profile](https://clawhub.ai/user/new-ironman)
- [MaxHub API website](https://www.aconfig.cn)
- [Video & User API reference](references/api-video-user.md)
- [Parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured tables or bullet summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English responses; keeps API key values out of output; presents API-derived data with concise summaries.]

## Skill Version(s):

3.6.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
