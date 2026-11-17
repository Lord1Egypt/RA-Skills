## Description:

Twitter/X 数据查询助手，支持查询推文详情、用户资料、搜索结果、评论和趋势数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, media teams, marketing teams, and developers use this skill to collect and summarize Twitter/X public conversation signals, including tweet details, comments, user profiles, search timelines, and trending topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Twitter/X search terms, handles, tweet IDs, and the MaxHub API key to a third-party API service.

Mitigation: Use only if that data sharing is acceptable, avoid sensitive queries, keep API keys out of outputs, and prefer a pinned skill version.

Risk: Shell-based API calls may fail or query unintended endpoints if paths or parameters are guessed.

Mitigation: Construct requests only from documented Twitter endpoint paths and encode user-supplied parameters before making HTTP requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/twitter-aggregate-scraper)
- [MaxHub API website](https://www.aconfig.cn)
- [Tweet Data API](artifact/references/api-tweet.md)
- [Search & Trending API](artifact/references/api-search-trending.md)
- [Parameter Mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summaries with tables, links, and inline shell commands for API access and configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs follow the user's language, hide API key values, and summarize returned API data without writing to Twitter/X.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
