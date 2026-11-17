## Description:

抓取公开微博用户在指定日期发布的帖子内容，支持长文全文获取和滚动加载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[x1a0f31](https://clawhub.ai/user/x1a0f31)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect public posts from a specified Weibo account for a requested date range, including expanded long-form posts when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect posts for broadly phrased Weibo scraping requests, which may target the wrong account or date range if the request is ambiguous.

Mitigation: Confirm the target user and date range before browser automation begins.

Risk: The workflow is intended for public Weibo pages and could be misused for private, logged-in, or non-consensual data collection.

Mitigation: Limit use to public pages visible without login and decline requests involving private or non-consensual collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x1a0f31/skills/weibo-scraper)
- [Weibo mobile search URL pattern](https://m.weibo.cn/search?luicode=10000011&lfid=100103type%3D1%26q%3D{URL编码的昵称})
- [Weibo mobile profile URL pattern](https://m.weibo.cn/u/{UID})
- [Weibo mobile status URL pattern](https://m.weibo.cn/status/{微博ID})

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with numbered post entries and timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are sorted chronologically and limited to public Weibo content visible through browser access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
