## Description: <br>
个股分析大师：面向A股支持单股深度分析与多股对比（综合/技术面/财报/价值面）。触发词：个股分析、个股对比、财报对比、价值分析、技术分析、买卖点、基本面、选时、ST分析。适用场景：用户需要对一个或多个明确股票标的做结构化分析与对比。不适用场景：未提供股票标的、仅做盘口超短交易指令、非A股标的。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate structured A-share single-stock analysis or 2-8 stock comparisons across fundamentals, technical signals, financial reports, valuation, capital flow, and ST-risk scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ratings, stop-losses, target prices, and entry conditions could be mistaken for personalized investment advice or automatic trading instructions. <br>
Mitigation: Treat outputs as informational analysis only, verify conclusions independently, and keep the included disclaimer that the content is not investment advice. <br>
Risk: The skill depends on daxiapi-cli market data and a DAXIAPI token, so stale data, unavailable fields, or token handling can affect analysis quality. <br>
Mitigation: Verify the data source and token storage before use, mark missing data clearly, and downgrade conclusions when required fields are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-stock-analysis) <br>
- [Report template](assets/report-template.md) <br>
- [CLI command reference](references/cli-commands.md) <br>
- [Error handling guide](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an explicit A-share stock target and current market or financial data where available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
