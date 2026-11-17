## Description:

Taiwan stock info using Fugle or FinMind APIs. Provides real-time quotes, historical data, financial statements, and technical indicators for Taiwan stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hans00](https://clawhub.ai/user/hans00)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to prepare Taiwan stock data requests and examples for real-time quotes, historical prices, financial statements, institutional activity, and technical indicators through Fugle and FinMind APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fugle API keys and FinMind tokens are sensitive credentials.

Mitigation: Use environment variables or a secret store for real credentials and avoid placing secrets in prompts, files, or shared command history.

Risk: API terms, authentication requirements, and rate limits may affect whether requests succeed or are permitted.

Mitigation: Review the Fugle and FinMind provider terms and current rate limits before using the generated API requests.

Risk: Stock data and technical indicators can be time-sensitive and may be unsuitable as sole support for financial decisions.

Mitigation: Validate returned data against the provider response and apply independent financial review before acting on analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hans00/skills/tw-stock-info)
- [Fugle API](https://api.fugle.tw)
- [FinMind API](https://api.finmindtrade.com/api/v4/data)
- [Fugle API specifications](api/fugle.md)
- [FinMind API specifications](api/finmind.md)
- [Usage examples](example.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with cURL examples and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoints, request parameters, authentication headers, and example JSON response shapes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
