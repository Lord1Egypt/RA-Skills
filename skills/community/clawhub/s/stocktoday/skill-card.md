## Description:

Helps agents retrieve, clean, compare, and export market and financial data across Chinese, Hong Kong, and U.S. securities and macroeconomic topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usa2046](https://clawhub.ai/user/usa2046)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial researchers can ask an agent to fetch and compare market, company, sector, fund, futures, options, bond, and macroeconomic data, then summarize findings or prepare reusable data exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because a proxy configuration can expose credentials over an unencrypted connection in some configurations.

Mitigation: Keep insecure HTTP disabled and use the documented HTTPS gateway hosts. Only enable an insecure endpoint when the operator understands and accepts the credential exposure risk.

## Reference(s):

- [API interface index](references/接口索引.md)
- [API usage notes](references/接口使用提示.md)
- [StockToday token registration](https://stocktoday.cn)
- [ClawHub skill page](https://clawhub.ai/usa2046/skills/stocktoday)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Code, Files, Guidance]

**Output Format:** [Markdown summaries and tables, pandas DataFrames, CSV or Parquet exports, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies with the requested instruments, interfaces, date range, and export size; requires a StockToday API token.]

## Skill Version(s):

2.4.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
