## Description:

基于TDX API的股票数据查询技能，提供全面的A股市场数据查询功能，包括实时行情、K线数据、分时数据、分时成交、股票搜索、指数数据、ETF数据、市场统计、个股新闻、股票公告等31个API接口。当用户询问股票相关信息时调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bensema](https://clawhub.ai/user/bensema)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query A-share market data through their configured TDX API service, including quotes, K-line history, intraday data, trades, stock search, indices, ETFs, market statistics, news, and announcements. It can also create and manage backend data-ingestion tasks when the configured service supports them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on user-configured stock-data API services, and the server security summary warns that plaintext endpoints are recommended in the artifact examples.

Mitigation: Operate only trusted API services, prefer HTTPS endpoints, isolate the runtime, and pin dependencies as recommended by the server security guidance.

Risk: Task-creation and cancellation methods can start backend ingestion jobs and may leave stored data behind.

Mitigation: Treat task-management calls as privileged operations and review requested task scope, storage paths, and cancellation behavior before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bensema/skills/tdx-api-skill)
- [Publisher profile](https://clawhub.ai/user/bensema)
- [README.md](artifact/README.md)
- [TEST_REPORT.md](artifact/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TDX_API_URL for core queries; AKSHARE_API_URL is optional for news and disclosure queries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
