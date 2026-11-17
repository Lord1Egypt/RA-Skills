## Description:

Stocktoday Data helps agents retrieve and analyze A-share, Hong Kong, U.S., fund, futures, options, bond, and macro market data through 235+ Tushare-compatible StockToday interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usa2046](https://clawhub.ai/user/usa2046)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to turn market research requests into data retrieval, cleaning, comparison, screening, export, and Markdown summary workflows for equities, funds, derivatives, bonds, and macro data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-backed market-data requests can be routed through the StockToday gateway or a user-configured gateway.

Mitigation: Install only if you trust StockToday's gateway, keep tokens in environment variables, and do not set TUSHARE_GATEWAY to an untrusted host.

Risk: A documented HTTP backup gateway could expose API tokens or request data over plaintext transport.

Mitigation: Use the HTTPS gateway, avoid the documented HTTP backup gateway, and rotate any token previously sent through an unknown or plaintext gateway.

Risk: The skill depends on version ranges for tushare and pandas, which can change behavior over time.

Mitigation: Pin and review dependency versions before production use.

Risk: Market-data responses can be empty, delayed, permission-limited, or noisy for non-trading days and single-day signals.

Mitigation: Check the trading calendar, data timestamp, row counts, and access tier before presenting results or drawing conclusions.

## Reference(s):

- [StockToday data API reference](artifact/references/数据接口.md)
- [StockToday website](https://stocktoday.cn)
- [StockToday Tushare-compatible gateway](https://tushare.citydata.club/)
- [ClawHub skill page](https://clawhub.ai/usa2046/skills/stocktoday-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown summaries with tables, Python snippets, shell commands, and optional CSV or Parquet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require TUSHARE_TOKEN and network access to StockToday or Tushare-compatible endpoints.]

## Skill Version(s):

2.0.2 (source: release evidence, artifact frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
