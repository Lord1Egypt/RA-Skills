## Description:

获取ZAKER聚合权威媒体的最新头条新闻与热点资讯。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaker-coder](https://clawhub.ai/user/zaker-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current ZAKER hot-news headlines and summarize major domestic, global, breaking, or trending news items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger examples may cause vague requests about what is new or interesting to be handled as news requests.

Mitigation: Confirm user intent when a request could reasonably refer to non-news topics.

Risk: The skill contacts the documented ZAKER API to retrieve current public headlines.

Mitigation: Disclose network access and avoid sending private user data to the endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaker-coder/skills/zaker-hot-news)
- [ClawHub publisher profile](https://clawhub.ai/user/zaker-coder)
- [ZAKER hot articles API](https://skills.myzaker.com/api/v1/article/hot?v=1.0.3)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown headline list with article titles, links, summaries, authors, and optional JSON from the ZAKER API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches the latest 20 hot articles from the documented public ZAKER endpoint.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter says 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
