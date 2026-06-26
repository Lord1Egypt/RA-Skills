## Description: <br>
Fetches Upbit quotation and market data through CLI commands for trading pairs, candles, trades, tickers, orderbooks, and watchlist tickers with JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuns9](https://clawhub.ai/user/kuns9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current Upbit market data from the Upbit Open API for analysis, monitoring, and workflow automation. It is intended for run-once CLI execution where the agent consumes structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make network requests to a configurable Upbit API base URL. <br>
Mitigation: Keep the baseUrl configured as https://api.upbit.com unless a trusted reviewer approves another endpoint. <br>
Risk: The configuration supports optional accessKey and secretKey fields. <br>
Mitigation: Leave credentials blank for market-data commands unless a future authenticated command explicitly requires them. <br>
Risk: The --config option can point the CLI at an arbitrary local JSON file. <br>
Mitigation: Use a dedicated skill configuration file and avoid passing unrelated local files as configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kuns9/upbit-market-data-skill) <br>
- [Upbit REST API guide](https://docs.upbit.com/kr/reference/rest-api-guide) <br>
- [Upbit JWT authentication reference](https://docs.upbit.com/kr/reference/auth) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API calls, Market data] <br>
**Output Format:** [JSON success objects on stdout and JSON error objects on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include Upbit response payloads; failed requests include structured error details and exit code 1.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
