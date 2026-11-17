## Description:

计算股票或组合的年化收益率，支持按股票代码和日期范围自动拉取K线计算，也支持直接输入初始和最终资金计算，并输出年化收益率、总收益率、最大回撤、夏普比率等绩效报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangqirun](https://clawhub.ai/user/kangqirun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to calculate stock or portfolio annualized return and related performance metrics from either stock-code/date inputs or direct capital values. The skill is aimed at Chinese-language A-share analysis workflows and includes a financial disclaimer that results are informational, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-code/date mode may send stock symbols, date ranges, and related financial query details to the declared external stock-data service using BITSOUL_TOKEN.

Mitigation: Use direct capital-input mode for calculations that should avoid remote stock-data lookup, and configure BITSOUL_TOKEN only in trusted environments.

Risk: Generated performance metrics can be mistaken for investment advice or future-return guarantees.

Mitigation: Present outputs as informational analysis only and retain the skill's disclaimer that results do not constitute investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kangqirun/skills/stock01)
- [BitSoul homepage](https://www.aicodingyard.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown performance report with metric table and brief conclusion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BITSOUL_TOKEN for remote stock-data lookup; direct capital-input mode can be used without sending stock-query details to the external data service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
