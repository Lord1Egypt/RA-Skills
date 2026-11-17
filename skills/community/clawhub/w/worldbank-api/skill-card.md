## Description:

Fetch country-level economic and development data (GDP, population, inflation, unemployment, life expectancy, CO2, poverty, trade...) with the free World Bank Indicators API (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to fetch public country-level World Bank economic and development indicators, compare countries or aggregates, and retrieve historical time-series data without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Country codes, indicator codes, date ranges, and search keywords may be sent to api.worldbank.org.

Mitigation: Avoid confidential query terms and review network egress requirements before use in sensitive environments.

Risk: World Bank data can be lagged, revised, missing, or returned as null for recent periods.

Mitigation: Use latest non-empty queries where appropriate, check response metadata such as lastupdated, and report dates alongside values.

Risk: Invalid, archived, or unsupported indicators can produce API error envelopes instead of usable data.

Mitigation: Check API error messages, search for successor indicators, and validate indicator and country codes before relying on results.

## Reference(s):

- [World Bank Indicators API](https://api.worldbank.org/v2)
- [World Bank API - Full Endpoint Reference](references/endpoints.md)
- [Verified Indicator Codes by Topic](references/indicators.md)
- [ClawHub Skill Page](https://clawhub.ai/nanookai/skills/worldbank-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API URLs, code examples, and optional JSON data output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper can print human-readable tables or raw JSON rows from the World Bank API.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
