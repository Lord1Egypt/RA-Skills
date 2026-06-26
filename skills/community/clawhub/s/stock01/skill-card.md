## Description: <br>
计算股票或组合的年化收益率，支持按股票代码和日期范围自动拉取K线计算，也支持直接输入初始和最终资金计算，并输出年化收益率、总收益率、最大回撤、夏普比率等绩效报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangqirun](https://clawhub.ai/user/kangqirun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to calculate A-share stock or portfolio performance from stock codes, date ranges, price data, or capital values. It is suited for reference analysis of annualized return, total return, drawdown, and Sharpe ratio, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access token-backed market data when calculating stock or portfolio performance. <br>
Mitigation: Keep BITSOUL_TOKEN private, scope it where possible, and configure the skill only in environments where this finance-calculation behavior is intended. <br>
Risk: Finance-related prompts can be vague, which may cause the skill to activate more broadly than intended. <br>
Mitigation: Use stricter trigger rules or ask for confirmation before using the skill for ambiguous finance conversations. <br>
Risk: The generated performance report can be mistaken for investment advice. <br>
Mitigation: Present results as reference calculations and retain a clear disclaimer that the output is not investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kangqirun/stock01) <br>
- [BitSoul token registration and homepage](https://www.aicodingyard.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown performance report with optional Python code snippets and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include annualized return, total return, maximum drawdown, Sharpe ratio, short conclusions, and a disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
