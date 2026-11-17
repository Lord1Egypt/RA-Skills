## Description:

Access real-time and historical stock market data via Alpha Vantage API. Get quotes, time series, technical indicators, fundamentals, forex, crypto, and commodities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to retrieve Alpha Vantage market data for stocks, forex, crypto, commodities, economic indicators, news, and technical analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data queries and Alpha Vantage API keys are sent to Alpha Vantage.

Mitigation: Install only when that data sharing is acceptable for the intended workflow.

Risk: Passing an API key with --key can expose the credential through shell history or process listings.

Mitigation: Prefer setting the ALPHA_VANTAGE_KEY environment variable instead of passing secrets on the command line.

Risk: Broad stock-market trigger phrases may cause the skill to be considered for generic market-data requests.

Mitigation: Confirm the intended data source and request scope before executing API-backed commands.

## Reference(s):

- [Stock Market Data Reference](references/api_coverage.md)
- [Alpha Vantage API](https://www.alphavantage.co)
- [Alpha Vantage Query Endpoint](https://www.alphavantage.co/query)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with bash command examples; the included CLI outputs JSON by default with optional CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Alpha Vantage API access; prefer ALPHA_VANTAGE_KEY for credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
