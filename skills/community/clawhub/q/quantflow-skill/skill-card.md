## Description:

Quantflow Skill helps agents turn Chinese natural-language financial research requests into executable Akshare and AKQuant workflows for data retrieval, cleaning, comparison, export, concise analysis, and strategy backtesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external agents use this skill to map Chinese financial questions about A-shares, indices, ETFs, funds, company financials, market sectors, capital flows, news, macro data, and backtests into structured data workflows and summarized research outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial data and backtest outputs may be mistaken for trading advice.

Mitigation: Present outputs as research support only, include data scope and limitations, and avoid direct buy/sell recommendations or automated trading actions.

Risk: The skill depends on networked data providers and external Python packages.

Mitigation: Install in an isolated virtual environment, pin and review `akshare` and `akquant` versions, and disclose incomplete or failed data retrieval segments.

Risk: Market data can be unavailable, delayed, incomplete, or affected by ambiguous Chinese security names.

Mitigation: Validate schemas and key fields, normalize dates and symbols, clarify ambiguous entities, and distinguish non-trading days, empty ranges, delisted securities, and parameter errors.

## Reference(s):

- [Quantflow Skill release page](https://clawhub.ai/yejinlei/skills/quantflow-skill)
- [Akshare data interface reference](artifact/references/数据接口.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown summaries with tables, Python snippets or scripts, shell commands, and optional CSV or Parquet file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data scope, source interface names, request parameters, retrieval time, row counts, field lists, failed segments, and analysis limitations when files are generated.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
