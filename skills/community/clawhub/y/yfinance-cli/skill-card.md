## Description: <br>
This skill helps agents fetch live Yahoo Finance market data through the yahoo-finance CLI for quotes, fundamentals, historical prices, options, movers, search, and portfolio value calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gddezero](https://clawhub.ai/user/gddezero) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill when an assistant needs current Yahoo Finance data instead of relying on memory. It supports quote lookup, fundamentals, historical OHLCV data, options chains, market screeners, ticker search, and portfolio value calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat market data or analyst fields as financial advice. <br>
Mitigation: Present the tool output as market data only and avoid framing it as an investment recommendation. <br>
Risk: The globally installed yahoo-finance command may not be the expected yahoo-finance2 package. <br>
Mitigation: Confirm the installed command before use in environments where command provenance matters. <br>
Risk: Yahoo Finance lookups can disclose requested symbols or portfolio holdings to an external data service. <br>
Mitigation: Use the skill only when the user is comfortable sending those lookup terms to Yahoo Finance. <br>
Risk: Invalid or incorrectly formatted symbols can produce undefined output or stale records instead of valid current JSON. <br>
Mitigation: Validate symbols, apply documented exchange-specific formatting rules, and check returned market and price fields before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gddezero/yfinance-cli) <br>
- [Publisher profile](https://clawhub.ai/user/gddezero) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; CLI command output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one symbol per CLI invocation; invalid symbols may return undefined instead of JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
