## Description: <br>
Stocktoday Data helps agents retrieve, compare, summarize, and export market and financial data through the Tushare Python API routed via the StockToday gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usa2046](https://clawhub.ai/user/usa2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to translate natural-language market research requests into Tushare-compatible Python calls for equities, funds, futures, options, bonds, macro data, financial statements, sector analysis, news, and exports. It is intended for data retrieval and analysis support, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A sensitive Tushare token and query history may be sent through the custom StockToday gateway. <br>
Mitigation: Install only when the user intentionally trusts StockToday, use an isolated or low-privilege token, and review the provider's logging, retention, and credential-protection practices before use. <br>
Risk: Unsafe HTTP backup endpoint guidance could expose tokens or query traffic in transit. <br>
Mitigation: Avoid HTTP gateways and use only HTTPS endpoints unless the environment has a separate trusted transport control. <br>
Risk: Market data may be unavailable, delayed, permission-limited, or empty for non-trading days. <br>
Mitigation: Include source interface, request parameters, timestamps, row counts, and missing-data or permission notes in user-facing outputs. <br>


## Reference(s): <br>
- [Data Interface Reference](references/数据接口.md) <br>
- [StockToday Tushare Gateway](https://tushare.citydata.club/) <br>
- [ClawHub Skill Page](https://clawhub.ai/usa2046/stocktoday-py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown summaries with concise tables, Python code snippets, optional shell commands, and optional CSV or Parquet file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include data scope, source interface, request parameters, retrieval time, row counts, field lists, and any missing-data or permission limits when files are generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
