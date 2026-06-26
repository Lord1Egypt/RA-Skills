## Description: <br>
Retrieve and interpret World Bank annual development, macroeconomic, and demographic indicators with country comparisons and citation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents through World Bank Open Data indicator discovery, country comparisons, annual time-series retrieval, interpretation, and citation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: World Bank data is annual and may not contain the latest quarter, month, day, or ticker-level value. <br>
Mitigation: Use this skill for annual World Bank indicators only; direct real-time, market, firm-level, or high-frequency questions to a more appropriate data source. <br>
Risk: Missing observations can be confused with real zero values. <br>
Mitigation: Treat null values as data not available, report the observed year explicitly, and never substitute zero or invent figures. <br>
Risk: Incorrect indicator or country codes can produce invalid requests or misleading results. <br>
Mitigation: Search indicators, resolve country codes, confirm metadata and units, and retry invalid-parameter errors only after correcting the request. <br>
Risk: The generic passthrough can be misapplied outside the intended World Bank API scope. <br>
Mitigation: Use the passthrough only for relative World Bank /v2 endpoints and keep the MCP server environment empty unless setting non-secret tuning values. <br>


## Reference(s): <br>
- [World Bank API Basic Call Structure](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) <br>
- [World Bank Indicator Browser](https://data.worldbank.org/indicator) <br>
- [Endpoints & Tools](reference/endpoints.md) <br>
- [Best Practices](reference/best-practices.md) <br>
- [Response Fields](reference/response-fields.md) <br>
- [Common Errors](reference/common-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, API calls] <br>
**Output Format:** [Markdown guidance with tables, citation templates, and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; outputs emphasize annual data, units, null handling, and source citations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
