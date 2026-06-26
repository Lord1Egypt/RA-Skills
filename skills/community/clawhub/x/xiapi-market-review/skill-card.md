## Description: <br>
A股市场全面复盘，整合指数表现、板块热力图、涨跌停、风格轮动、市场温度分析。触发词：市场复盘、今天市场怎么样、市场分析、每日复盘、市场概览。适用场景：对当日A股市场进行全面复盘、生成综合市场分析报告。不适用场景：个股深度分析、单一指标分析、债券/基金分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate a same-day A-share market recap that combines index performance, sector heatmaps, limit-up/limit-down activity, style rotation, market temperature, and related findings into a structured report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a DAXIAPI token and may expose credentials if users paste tokens into chat transcripts. <br>
Mitigation: Configure credentials outside shared transcripts where possible, prefer environment variables or trusted local CLI configuration, and avoid echoing token values. <br>
Risk: The workflow runs the external npm package daxiapi-cli with @latest, which can change behavior between runs. <br>
Mitigation: Install only if DAXIAPI is trusted, review the CLI before use when needed, and pin a known version for controlled environments. <br>
Risk: Market data may be delayed, unavailable on non-trading days, or inconsistent across dimensions. <br>
Mitigation: Label data timestamps, disclose missing or stale data, cross-check dimensions, and present uncertain conclusions as conditional analysis. <br>
Risk: A market recap can be mistaken for individualized investment advice. <br>
Mitigation: Keep the report neutral, include risk warnings and disclaimers, avoid deterministic predictions, and use the skill only for explicit A-share market recap requests. <br>


## Reference(s): <br>
- [DAXIAPI](https://daxiapi.com) <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-market-review) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with tables, inline shell commands, risk notes, and disclaimer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DAXIAPI market data via npm CLI commands and should label data timestamps, missing data, and analysis limitations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
