## Description:

Provides 276 Tushare-compatible market data interfaces for researching Chinese, Hong Kong, and US equities, funds, derivatives, bonds, and macroeconomic data through StockToday.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usa2046](https://clawhub.ai/user/usa2046)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts can retrieve and compare market, financial, sector, capital flow, news, and macroeconomic data, then prepare summaries, exports, or reusable analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may cause the skill to activate for requests outside its intended financial data use, and dependency versions are not fully specified.

Mitigation: Use it for explicit financial data requests and review the selected dependency versions before installation, as advised by the security assessment.

Risk: The security scan was partial because some local references could not be resolved, so its findings may be incomplete.

Mitigation: Review the unresolved references and reassess the skill before relying on the scan as a complete security review.

## Reference(s):

- [StockToday data service](https://stocktoday.cn)
- [StockToday Tushare-compatible gateway](https://tushare.citydata.club/)
- [Data interface reference (Chinese)](artifact/references/数据接口.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Files]

**Output Format:** [Markdown summaries and tables, Python workflows, and CSV or Parquet data exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data requests require a user-provided TUSHARE_TOKEN.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
