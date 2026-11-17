## Description:

研林Skill — 采集A股大盘指数、行业板块排名、核心权重股行情数据

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial-analysis agents use this skill to fetch current A-share index quotes, sector rankings, and core stock quotes for market summaries and downstream reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data may be incomplete, delayed, or fetched from unauthenticated public endpoints, including one HTTP sector-ranking source.

Mitigation: Use the output for informational lookup and verify it against authoritative HTTPS or authenticated data sources before trading or other high-stakes decisions.

Risk: The skill output could be mistaken for financial advice when used in summaries or reports.

Mitigation: Present results as market data only and add human review before using them for investment recommendations.

## Reference(s):

- [Sina Finance quote endpoint](https://hq.sinajs.cn/list={codes})
- [Sina Finance](https://finance.sina.com.cn)
- [Tonghuashun sector rankings](http://q.10jqka.com.cn/thshy/)
- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanlin-market-data)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON or plain text market-data report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public market data and prints the result to standard output.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
