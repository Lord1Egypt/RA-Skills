## Description: <br>
Access real-time and historical market data from the Alpha Vantage API, including quotes, time series, technical indicators, fundamentals, forex, cryptocurrency, commodities, news, and economic indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve market, company, currency, crypto, commodity, economic, and technical-analysis data through a local Alpha Vantage CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Alpha Vantage and may consume API quota or expose an API key if passed directly on the command line. <br>
Mitigation: Set ALPHA_VANTAGE_KEY in the environment, protect the key, and monitor Alpha Vantage quota usage. <br>
Risk: Broad stock and market triggers may invoke the skill for generic finance questions where live API calls are unnecessary. <br>
Mitigation: Use the skill only when market data retrieval from Alpha Vantage is intended. <br>


## Reference(s): <br>
- [Alpha Vantage API](https://www.alphavantage.co) <br>
- [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key) <br>
- [Stock Market Data Reference](references/api_coverage.md) <br>
- [ClawHub skill page](https://clawhub.ai/raychanpmp/stockmarket) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Data] <br>
**Output Format:** [JSON by default, with optional CSV output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to Alpha Vantage; uses ALPHA_VANTAGE_KEY from the environment or a --key argument, falling back to the Alpha Vantage demo key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
