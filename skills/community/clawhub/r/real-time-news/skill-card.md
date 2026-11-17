## Description:

实时新闻 provides agent tools for querying real-time hot lists and news trends from multiple Chinese platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize real-time hot lists from platforms such as Weibo, Baidu, Zhihu, Toutiao, 36Kr, Tencent News, Bilibili, Douyin, Hupu, Huxiu, and Juejin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Xiaobenyang API key and stores it persistently in a local plaintext .env file.

Mitigation: Use an isolated workspace and a low-privilege or revocable key, then delete or rotate the key after use.

Risk: The skill relies on an external Xiaobenyang API for real-time news data.

Mitigation: Review returned data before relying on it, and do not fabricate news results when the API key is missing or the upstream call fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/real-time-news)
- [Xiaobenyang API key service](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls]

**Output Format:** [Markdown-formatted summaries of raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key; returned content depends on upstream real-time news APIs.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
