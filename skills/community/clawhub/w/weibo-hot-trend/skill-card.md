## Description:

获取微博热搜榜数据，返回热搜标题、热度值和跳转链接。当用户需要查看微博热搜、微博热点、微博热榜时使用此技能。支持自定义获取条数（默认50条）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[geniuslishengbo](https://clawhub.ai/user/geniuslishengbo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current Weibo hot-search topics, heat values, labels, and search links from Weibo's public web endpoint. It supports an optional result-count argument and defaults to 50 entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes a direct HTTPS request to Weibo and prints remote hot-search text in the terminal.

Mitigation: Install only when this network behavior is acceptable, and review terminal output before relying on it.

Risk: Remote responses may be malformed, unexpectedly large, or served with an unexpected status or content type.

Mitigation: Add response-size limits, HTTP status checks, and content-type checks before deployment in stricter environments.

Risk: Very frequent polling may trigger Weibo rate limiting or anti-abuse controls.

Mitigation: Follow the artifact guidance to space requests by at least 30 minutes unless the publisher documents a safer cadence.

Risk: The optional result-count argument is only loosely parsed.

Mitigation: Validate the argument as a bounded positive integer before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geniuslishengbo/skills/weibo-hot-trend)
- [Weibo hot search page](https://weibo.com/hot/search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text with ranked Weibo hot-search entries, heat values, labels, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional numeric result limit; defaults to 50 entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
