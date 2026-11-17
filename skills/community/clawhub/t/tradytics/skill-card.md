## Description:

Pull market, options, dark-pool, fundamentals, filings, disclosures, calendar, news, screening, signal, and prediction-market data through the Tradytics API, and help users query and interpret those responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tradytics](https://clawhub.ai/user/tradytics)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to retrieve and interpret Tradytics market data or write Python and JavaScript code against the API and SDKs. It supports research and monitoring workflows across options activity, equities, company fundamentals, and market calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-scoped endpoints can read linked portfolio, trades, backtests, dashboards, and watchlists; some referenced material was not fully inspected according to the security assessment.

Mitigation: Review the relevant endpoint documentation and grant account scope only when this data access is intended.

Risk: The API key is sent as a request query parameter and could be exposed if request URLs are printed or logged.

Mitigation: Load the key from the user's private configuration and never print, log, or write it into files.

## Reference(s):

- [Tradytics API documentation](https://tradytics.com/docs)
- [Tradytics OpenAPI specification](https://tradytics.com/api/public/v1/openapi.json)
- [Tradytics skill release](https://clawhub.ai/tradytics/skills/tradytics)
- [Account data endpoint reference](artifact/references/account.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Code, Shell commands, Configuration guidance, API calls]

**Output Format:** [JSON market-data responses, Markdown summaries, and Python, JavaScript, or HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries; preserve response timestamps, pagination cursors, units, and null values when presenting data.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
