## Description:

分析A股涨停、跌停和炸板股票数据，帮助识别短线热点板块、市场情绪和连板龙头股。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to fetch DAXIAPI A-share limit-up, limit-down, and broken-limit data, summarize sector heat, identify leading consecutive-limit stocks, and produce a short structured trading-reference report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run a mutable third-party CLI package and provide it with an API token.

Mitigation: Review and pin a trusted DAXIAPI CLI version before use, keep the token out of shell history and logs, and rotate any token used with an unreviewed latest package.

Risk: The generated analysis may influence short-term trading decisions and can be wrong, stale, or incomplete.

Mitigation: Require the report to state the data date, include risk notes and a disclaimer, and treat findings as reference material rather than investment advice.

## Reference(s):

- [DAXIAPI](https://daxiapi.com)
- [CLI 命令参考](references/cli-commands.md)
- [Token 配置指南](references/token-setup.md)
- [字段说明](references/field-descriptions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, concise findings, risk notes, disclaimer, and optional shell commands for DAXIAPI CLI setup or data retrieval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current DAXIAPI data and a configured API token; analysis is for reference only and should not be treated as investment advice.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
