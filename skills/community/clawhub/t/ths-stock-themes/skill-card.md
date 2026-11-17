## Description:

获取同花顺个股题材/概念板块和人气排名数据。使用场景：(1) 查询单只股票在同花顺的题材/概念分类，(2) 获取同花顺个股人气排名榜单，(3) 生成包含题材和人气信息的 Markdown 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinelp100](https://clawhub.ai/user/shinelp100)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Tonghuashun stock themes, concept sectors, and popularity rankings for Chinese stock-market research, then generate Markdown reports or JSON summaries. Results should be treated as informational market data, not financial advice.

### Deployment Geography for Use:

Global; data sources focus on China-market stocks.

## Known Risks and Mitigations:

Risk: Market data and popularity rankings may be stale, incomplete, or affected by source-site page changes.

Mitigation: Verify important outputs against the live Tonghuashun or iWenCai source pages before relying on them.

Risk: Generated reports could be mistaken for investment advice.

Mitigation: Label outputs as informational market-data summaries and apply independent financial review for investment decisions.

Risk: Included scripts may return placeholder or empty data when browser-based collection is not performed.

Mitigation: Check for empty result sets and confirm browser collection succeeded before using or sharing a report.

## Reference(s):

- [Implementation Details](references/implementation.md)
- [Tonghuashun Stock Page Example](https://stockpage.10jqka.com.cn/000001/)
- [iWenCai Popularity Ranking Query](https://www.iwencai.com/unifiedwap/result?w=个股人气排名)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports, JSON objects, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamped public market-data summaries; included scripts may return placeholder or empty data unless paired with browser-based data collection.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
