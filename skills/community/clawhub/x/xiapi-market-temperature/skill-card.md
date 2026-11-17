## Description:

分析A股市场温度指标，通过估值温度、恐贪指数、趋势温度、动量温度判断市场冷热程度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to fetch DAXIAPI A-share market temperature data and produce structured valuation, sentiment, trend, momentum, and style-rotation analysis. The output is general market commentary and timing context, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to run mutable remote npm code via daxiapi-cli@latest.

Mitigation: Review the CLI before use and prefer pinning daxiapi-cli to a reviewed exact version.

Risk: API tokens could be exposed through URLs, shell history, transcripts, startup files, or local token storage.

Mitigation: Use bearer headers or a protected secret manager flow, avoid token-in-URL patterns, and keep tokens out of shared logs and shell startup files.

Risk: Market analysis output may be mistaken for personalized investment advice.

Mitigation: Frame reports as general market commentary, include the disclaimer, and avoid absolute or deterministic trading language.

Risk: Delayed or abnormal market data can lead to misleading conclusions, including fear-greed values of 0 before refresh.

Mitigation: Check data dates and completeness, flag stale or unavailable data, and do not interpret a pre-refresh 0 value as extreme fear.

## Reference(s):

- [CLI 命令参考](references/cli-commands.md)
- [API 参考文档](references/api-reference.md)
- [Token 配置指南](references/token-setup.md)
- [字段说明](references/field-descriptions.md)
- [DAXIAPI](https://daxiapi.com)
- [DAXIAPI market temperature endpoint](https://daxiapi.com/coze/get_market_temp)
- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-market-temperature)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown market analysis report with tables, CLI commands, token setup guidance, risk notes, and a disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DAXIAPI token and current market data; reports should label data date and data source.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
