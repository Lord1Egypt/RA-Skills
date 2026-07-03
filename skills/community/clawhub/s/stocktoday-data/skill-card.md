## Description: <br>
Stocktoday Data helps agents fetch, clean, compare, screen, and export StockToday-compatible financial market data across equities, funds, futures, options, bonds, macroeconomic data, announcements, and news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usa2046](https://clawhub.ai/user/usa2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to turn natural-language market research requests into StockToday/Tushare-compatible API calls and concise financial data summaries, comparisons, exports, or reusable Python workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a StockToday API token and sends requests to a StockToday gateway. <br>
Mitigation: Keep TUSHARE_TOKEN in an environment variable or secret manager, do not paste real tokens into chat or shared files, and use the documented HTTPS gateway by default. <br>
Risk: The artifact documents an HTTP backup gateway, which can expose traffic to weaker transport security if selected. <br>
Mitigation: Avoid the HTTP backup gateway unless a user has explicitly accepted that network posture and has a compensating control. <br>
Risk: Market data analysis can be mistaken for financial advice or treated as a prediction. <br>
Mitigation: Frame results as data support, include scope and limitations, and avoid claims of guaranteed returns or trading outcomes. <br>
Risk: Financial data may be empty, delayed, permission-limited, or affected by non-trading days and API limits. <br>
Mitigation: Report the queried date range, source interface, row count, missing values, and failed segments, and verify important decisions against authoritative sources. <br>


## Reference(s): <br>
- [Stocktoday Data skill page](https://clawhub.ai/usa2046/skills/stocktoday-data) <br>
- [Publisher profile](https://clawhub.ai/user/usa2046) <br>
- [StockToday account and token service](https://stocktoday.cn) <br>
- [StockToday Tushare-compatible gateway](https://tushare.citydata.club/) <br>
- [StockToday data interface reference](references/数据接口.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with tables, inline Python or shell snippets, and optional CSV or Parquet file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state data scope, source interface, request parameters, row counts, fields, missing data, and failed segments when files are generated.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
