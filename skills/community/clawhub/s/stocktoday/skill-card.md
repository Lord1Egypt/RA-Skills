## Description:

Helps agents retrieve, compare, analyze, and export financial data for Chinese, Hong Kong, and U.S. markets, funds, futures, options, bonds, and macroeconomic indicators through 275 Tushare-compatible interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usa2046](https://clawhub.ai/user/usa2046)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial researchers use this skill to answer market, company, sector, capital-flow, news, and macroeconomic questions, compare securities, and export selected datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling the insecure gateway option can bypass the stated server restriction and expose the API token and financial data when using HTTP.

Mitigation: Use the default HTTPS gateway and leave TUSHARE_GATEWAY_ALLOW_INSECURE unset. Before using an alternate gateway, have the publisher enforce destination restrictions independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/usa2046/skills/stocktoday)
- [StockToday](https://stocktoday.cn)
- [StockToday data gateway](https://tushare.citydata.club/)
- [Interface usage notes](artifact/references/接口使用提示.md)
- [Data interface reference](artifact/references/数据接口.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Markdown, Files, Code]

**Output Format:** [Markdown summaries and tables; optionally CSV or Parquet data files and Python scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include selected financial indicators, comparisons, date ranges, and optional local data exports.]

## Skill Version(s):

2.3.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
