## Description: <br>
Use Twelve Data REST/WebSocket APIs for market quotes, latest prices, historical time series, symbol discovery, and technical indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softtrymee](https://clawhub.ai/user/softtrymee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to construct Twelve Data REST and WebSocket requests for live and historical multi-asset market data. It supports quotes, latest prices, time series, symbol discovery, technical indicators, and selected fundamentals endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed through URLs, logs, browser history, or shell history when query-string authentication examples are used. <br>
Mitigation: Prefer the Authorization header examples, keep TWELVEDATA_API_KEY in a secure environment variable, and avoid sharing full request URLs. <br>
Risk: Unbounded or repeated market-data requests can consume Twelve Data API credits or hit rate limits. <br>
Mitigation: Monitor API credit usage, cache frequent reads, and apply retry/backoff for transient failures and 429 responses. <br>


## Reference(s): <br>
- [Twelve Data documentation](https://twelvedata.com/docs) <br>
- [Twelve Data request guide](https://support.twelvedata.com/en/articles/5620512-how-to-create-a-request) <br>
- [Twelve Data trial information](https://support.twelvedata.com/en/articles/5335783-trial) <br>
- [ClawHub skill page](https://clawhub.ai/softtrymee/twelve-data) <br>
- [Publisher profile](https://clawhub.ai/user/softtrymee) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TWELVEDATA_API_KEY for authenticated Twelve Data requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
