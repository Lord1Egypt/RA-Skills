## Description:

Retrieve and interpret World Bank annual development, macroeconomic, and demographic indicators with country comparisons and citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through selecting World Bank indicators, fetching annual country or aggregate time series, interpreting missing values and units, comparing countries, and citing reported figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied country, indicator, and search terms may be sent to the World Bank API through the paired MCP server.

Mitigation: Avoid sending sensitive user text as lookup terms and keep requests limited to the country, indicator, and date parameters needed for the answer.

Risk: The paired worldbank-mcp package is outside this Markdown skill artifact.

Mitigation: Verify the MCP server package separately before deployment and confirm its configured environment remains empty unless optional tuning values are intentionally set.

Risk: World Bank data is annual and recent years can be null or unpublished.

Mitigation: Use mrv or explicit date ranges, report null values as unavailable, include the observation year, and avoid using the skill for real-time, firm-level, ticker, or price data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/simonpierreboucher02/skills/worldbank-al)
- [World Bank API Basic Call Structure](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392)
- [World Bank Indicator Browser](https://data.worldbank.org/indicator)
- [Endpoints & Tools](reference/endpoints.md)
- [Indicators & Country Codes](reference/indicators-and-countries.md)
- [Response Fields](reference/response-fields.md)
- [Best Practices](reference/best-practices.md)
- [Common Errors](reference/common-errors.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration, Shell commands]

**Output Format:** [Markdown guidance with example JSON tool calls, tables, citations, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to use public World Bank annual data, cite each reported figure, handle nulls as missing values, avoid invented API keys, and distinguish countries from aggregates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
