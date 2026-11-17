## Description:

收集A股某行业全部上市公司资料，包括代码、名称、交易所、行业、财务数据、控股股东及持股比例。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wtjjacobj](https://clawhub.ai/user/wtjjacobj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to gather A-share industry company lists, shareholder data, and market fields for stock industry analysis workflows. Review collected financial metrics before relying on them for investment or reporting decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review reports that the implementation materially differs from the advertised stock-finance collection claims and may not return the advertised ROE, margin, debt, cash-flow, or growth fields.

Mitigation: Review outputs before using them for financial decisions, run the skill in an isolated environment, and validate critical metrics against trusted financial data sources.

Risk: The skill is expected to use outbound access to public stock-data APIs and third-party Python dependencies.

Mitigation: Use pinned minimal dependencies and run only in environments where outbound public market-data access is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wtjjacobj/skills/stock-industry-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python snippets and structured stock-data records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require baostock, akshare, and pandas; output can include industry stock lists, shareholder fields, and daily market data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
