## Description: <br>
Stocktoday Data helps agents retrieve, clean, compare, screen, summarize, and export A-share, Hong Kong, U.S. stock, fund, futures, options, bond, and macroeconomic data through StockToday's Tushare-compatible data gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usa2046](https://clawhub.ai/user/usa2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and financial-data analysts use this skill to turn natural-language market research requests into StockToday/Tushare-compatible data queries, analysis summaries, and optional local exports. It supports quote checks, financial statement review, company comparison, sector and fund-flow analysis, announcements, macro data, and reusable data-pull workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens and query traffic are sent through the StockToday gateway. <br>
Mitigation: Use the skill only when that routing is acceptable, provide tokens through environment variables or explicit runtime parameters, and avoid exposing tokens in prompts or saved outputs. <br>
Risk: The artifact documents non-HTTPS backup gateway endpoints. <br>
Mitigation: Keep the gateway on the HTTPS endpoint unless a user explicitly approves another endpoint after reviewing the security tradeoff. <br>
Risk: The token_info diagnostic may reveal account or token status details. <br>
Mitigation: Run token_info only when account diagnostics are needed and avoid sharing its output beyond the current troubleshooting context. <br>
Risk: CSV or parquet export requests can write local files containing financial query results. <br>
Mitigation: Confirm export paths before writing files and include data scope, source interface, request parameters, and pull time in generated artifacts. <br>


## Reference(s): <br>
- [StockToday Data on ClawHub](https://clawhub.ai/usa2046/stocktoday) <br>
- [StockToday Token Registration](https://stocktoday.cn) <br>
- [StockToday Tushare-Compatible Gateway](https://tushare.citydata.club/) <br>
- [StockToday Data Interfaces](references/数据接口.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown summaries with tables, Python snippets, shell commands, and optional CSV or parquet files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a StockToday API token; exported files should include interface names, request parameters, pull time, row counts, fields, and missing-data notes.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
