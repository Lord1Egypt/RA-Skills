## Description:

小红书热门笔记搜索工具，支持关键词搜索获取热门内容数据，基于数据评分排序推荐热门笔记，助力创作者发现热门趋势、获取创作灵感。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand marketers, and MCN teams use this skill to search Xiaohongshu hot notes by keyword, compare popularity and relevance signals, discover related searches, and generate trend-oriented result tables and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and date filters are sent to Redfox through the bundled API client.

Mitigation: Avoid sensitive query terms, configure a revocable REDFOX_API_KEY, and rotate or revoke the key if it may have been exposed.

Risk: The generated HTML report path and report content may be unsafe if treated as trusted local output.

Mitigation: Use trusted output directories, avoid custom output paths for sensitive locations, and review generated HTML before opening or sharing it.

Risk: Calendar subscriptions may store search terms and schedules outside the immediate chat session.

Mitigation: Create subscriptions only for non-sensitive searches and review the reminder details before confirming them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/if530770/skills/xhs-explosive-content-detector)
- [Redfox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [Xiaohongshu hot article format reference](references/xhs_hot_article_format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown tables and guidance backed by JSON API results, with optional generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends search keywords, date filters, and pagination parameters to the Redfox API.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
