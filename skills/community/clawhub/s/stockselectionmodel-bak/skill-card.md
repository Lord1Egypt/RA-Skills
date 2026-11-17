## Description:

A股板块实时研报。全球新闻→A股映射、板块趋势研判、美股关联、利好利空、大事件提醒。零配置可用，输出兼容飞书/扣子/Markdown平台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujianbo0426](https://clawhub.ai/user/xujianbo0426)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate China A-share sector research, AI market briefings, and unusual-movement alerts from public market and news sources. Outputs are informational and are not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock content may be incorrect, stale, or interpreted as financial advice.

Mitigation: Treat reports as informational only, retain the provided disclaimer, and require human review before making investment decisions.

Risk: Reports directly render links from external news sources.

Mitigation: Review rendered links before sharing reports and avoid opening links from untrusted sources in privileged environments.

Risk: The skill performs outbound requests to market/news providers and may use an optional Tavily API key.

Mitigation: Install only where outbound stock/news queries are acceptable, scope the Tavily key appropriately, and avoid passing secrets in prompts or report text.

Risk: Generated reports include hardcoded Content Science branding.

Mitigation: Confirm that the branding is acceptable for the deployment context before publishing outputs to end users.

Risk: Report generation leaves local JSON data snapshots under .local.

Mitigation: Periodically remove local snapshots and avoid running the skill in directories where cached market/news data should not persist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xujianbo0426/skills/stockselectionmodel-bak)
- [Data Source Priority](references/source_list.md)
- [Sector Trend Prompt](references/sector_prompt.md)
- [AI Stock Brief Prompt](references/analysis_prompt.md)
- [A-share Stock Mapping](references/stock_mapping.md)
- [Tavily Search API](https://api.tavily.com/search)
- [Eastmoney Sector Search Endpoint](https://search-api-web.eastmoney.com/search/jsonp?cb=&param=)
- [Eastmoney Market Data Endpoint](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports and alerts, with JSON available from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional TAVILY_API_KEY for enhanced news search; writes fetched data snapshots under .local during report generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
