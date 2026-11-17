## Description:

小红书内容搜索工具。通过 browser 工具操控已登录的 Chrome，搜索小红书公开笔记，提取标题、正文、话题标签、点赞数，分析消费趋势。用于市场调研中的消费者趋势研究。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxarch1980](https://clawhub.ai/user/dxarch1980)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market researchers use this skill to search public Xiaohongshu notes through a logged-in browser session, extract note metadata and content snippets, and synthesize consumer trend insights for commercial market research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Xiaohongshu browser session to read public note content.

Mitigation: Keep the remote debugging browser session limited to this task and close or isolate the session after use.

Risk: Searches or collected snippets may expose sensitive or personal context if the browser account or queries are not constrained.

Mitigation: Avoid sensitive or personal searches and review collected snippets before using them in reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxarch1980/skills/xiaohongshu-search-cn)
- [Xiaohongshu search results](https://www.xiaohongshu.com/search_result?keyword=<keyword>&source=web_explore_feed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with browser commands and structured trend summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public note titles, authors, links, engagement counts, topic tags, excerpts, and synthesized trend insights.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
