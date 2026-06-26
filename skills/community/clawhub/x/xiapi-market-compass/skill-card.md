## Description: <br>
市场罗盘是一套 A 股市场三维结构分析系统，通过趋势结构、估值和情绪三个维度评估市场健康状态，并生成仓位管理建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate A-share market structure reports from market compass data, with emphasis on trend breadth, valuation, sentiment, and position-management guidance. It is intended for market-level analysis, not individual stock, sector, short-term timing, or bond-fund analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves data through an external daxiapi CLI/provider and the artifact examples use a latest package reference. <br>
Mitigation: Confirm trust in the provider before installation and pin a known daxiapi package version for repeatable execution. <br>
Risk: The skill may require a daxiapi token for data access. <br>
Mitigation: Treat the token as a secret, store it only through the provider's configuration mechanism, and avoid pasting it into generated reports or shared logs. <br>
Risk: Generated market reports can influence investment decisions and are based on historical market indicators. <br>
Mitigation: Use reports as informational analysis only, keep the included investment-risk disclaimer, and require human review before acting on position guidance. <br>


## Reference(s): <br>
- [字段说明](references/field-descriptions.md) <br>
- [分析框架详解](references/analysis-framework.md) <br>
- [报告模板](assets/report-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-market-compass) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown market analysis report with optional shell commands for data retrieval and token configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are informational, use Chinese market metric names, avoid deterministic predictions, and include an investment-risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
