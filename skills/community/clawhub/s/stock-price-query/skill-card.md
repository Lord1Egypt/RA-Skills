## Description:

Queries current stock quotes and market index data for A-shares, Hong Kong stocks, US stocks, and major indexes, with single-symbol and batch lookup support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjefferson](https://clawhub.ai/user/tjefferson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up stock symbols or common mapped stock names and return compact quote summaries for A-share, Hong Kong, US equities, and major market indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried stock symbols are sent to Tencent's public quote API.

Mitigation: Use the skill only when this third-party market-data request is acceptable, and avoid submitting symbols whose disclosure would be sensitive.

Risk: Hong Kong and US market data from the free public endpoint may be delayed, and non-trading periods may return recent close data.

Mitigation: Treat results as informational market data and verify time-sensitive or regulated decisions with an authorized market-data source.

Risk: The public endpoint may rate limit or fail due to network availability.

Mitigation: Use light retry behavior and clearly report unavailable or partial results rather than presenting missing data as current.

## Reference(s):

- [股票查询 API 参考文档](references/api-docs.md)
- [Tencent public quote API endpoint](https://qt.gtimg.cn/q={symbol})
- [ClawHub skill page](https://clawhub.ai/tjefferson/skills/stock-price-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [JSON from the query script and concise Markdown quote summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-symbol lookup or comma-separated batches up to 20 symbols; requires python3 and network access to Tencent's public quote API.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
