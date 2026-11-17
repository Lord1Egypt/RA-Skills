## Description:

小红书热门笔记搜索工具，支持关键词搜索获取热门内容数据，基于数据评分排序推荐热门笔记，助力创作者发现热门趋势、获取创作灵感。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brands, MCNs, and content operations teams use this skill to search recent Xiaohongshu trending notes, compare scored examples, generate local HTML reports, and identify content directions for topic research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Redfox API key for API access.

Mitigation: Install only when you are comfortable granting the key, keep it in environment configuration, and avoid exposing it in prompts, logs, or output files.

Risk: The skill writes local HTML reports and the security summary identifies concrete file-write and HTML-injection risks.

Mitigation: Open generated reports cautiously and prefer a fixed safe output directory until report escaping and filename handling are fixed.

Risk: Calendar subscriptions can persist search details.

Mitigation: Avoid sensitive keywords on shared systems and review subscription details before creating calendar tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/if530770/skills/xhs-explosive-detector)
- [Redfox Hub API key page](https://redfox.hk/dashboard/keys?source=clawhub)
- [Xiaohongshu hot article format](artifact/references/xhs_hot_article_format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML files, Shell commands, Guidance]

**Output Format:** [Markdown tables and prompts, JSON script output, and optional local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY for Redfox API access; default lookback is recent Xiaohongshu data within the supported 30-day window.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
