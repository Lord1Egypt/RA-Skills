## Description:

多源 AI 新闻聚合与热度排序技能，输出中文摘要、热度分级、来源链接和重要性解读。

This skill is ready for commercial/non-commercial use.

## Publisher:

[npm-ued](https://clawhub.ai/user/npm-ued)

### License/Terms of Use:

MIT-0

## Use Case:

External readers, product teams, engineers, and business users use this skill to generate Chinese AI news briefings across global and Chinese sources. It ranks current AI headlines, cites sources, and separates confirmed items from watch-list items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Current-news output can become incomplete or stale if the search window is too narrow.

Mitigation: Use the skill's default 24-hour window, expand to 72 hours when signal is sparse, and state any required region or language focus when invoking it.

Risk: Community-only signals can overstate unverified AI trends.

Mitigation: Keep community-only items in the watch list until they are cross-verified by first-party sources or mainstream reporting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/npm-ued/skills/toutiao)
- [推荐新闻源](references/sources.md)
- [信源目录](references/source-catalog.md)
- [检索词矩阵](references/search-matrix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown news roundup with ranked sections, source links, watch-list items, and collection statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default standard mode returns 15-25 items; quick returns 8-12 items and deep returns 25+ items.]

## Skill Version(s):

1.0.2 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
