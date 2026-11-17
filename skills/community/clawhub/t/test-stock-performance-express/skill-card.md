## Description:

查询 A 股上市公司业绩快报数据，支持沪深京股票，并在用户询问营收、净利润、EPS、ROE、同比增长或定期报告等财务指标时返回相关结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lv19944516](https://clawhub.ai/user/lv19944516)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up performance express data for a single A-share ticker across Shanghai, Shenzhen, and Beijing markets. It helps present revenue, profit, EPS, ROE, year-over-year changes, and reporting period data as a Markdown table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a configured market-data API when given a valid A-share ticker.

Mitigation: Keep BASE_URL at the default unless the installer intentionally trusts another endpoint.

Risk: Broad finance keywords may cause the agent to consider this skill during general finance conversations.

Mitigation: Use the skill only when the user asks for A-share performance express or related financial metric lookup.

Risk: Returned financial data may be unavailable, incomplete, delayed, or null for some reporting periods.

Mitigation: Present unavailable values as missing data and avoid treating the table as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lv19944516/skills/test-stock-performance-express)
- [Configured market data API](https://market.ft.tech)
- [Publisher profile](https://clawhub.ai/user/lv19944516)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown table with brief status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one stock code in the form 6 digits plus .SH, .SZ, or .BJ; output depends on the configured market-data API.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
