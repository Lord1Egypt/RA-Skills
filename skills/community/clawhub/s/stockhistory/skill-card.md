## Description:

按代码与时间范围查历史日线，或查列表与详情，便于 K 线与走势分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query JisuAPI for historical daily stock prices, stock lists, and single-stock details by stock code and optional date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock codes, date ranges, and the configured JISU_API_KEY are sent to JisuAPI when the skill runs.

Mitigation: Use the skill only when sharing those query details with JisuAPI is acceptable, and prefer a dedicated API key with quota or billing limits.

Risk: Returned market data may be incomplete, stale, or unsuitable as financial advice.

Mitigation: Treat outputs as data lookup results for analysis or charting, and verify important market decisions against authoritative financial sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/stockhistory)
- [JisuAPI stock history API documentation](https://www.jisuapi.com/api/stockhistory/)
- [JisuAPI homepage](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script prints JSON responses from JisuAPI or JSON-formatted error objects.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
