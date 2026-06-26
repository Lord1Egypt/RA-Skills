## Description: <br>
Provides commands intended to query stock and ETF data, return basic market information, and produce stock recommendations for A-share, Hong Kong, U.S., and ETF markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinewilzhang](https://clawhub.ai/user/shinewilzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to ask an agent for stock prices, ETF information, watchlist-style queries, and stock recommendation output. Outputs should be treated as informational only and not used as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data and recommendation outputs may be unverified because the security evidence says the implementation calls an undocumented mock stock API. <br>
Mitigation: Review the skill before installing, validate results against trusted market data sources, and do not rely on its output for investment decisions. <br>
Risk: Ticker symbols, ETF names, and query terms may be sent to api.mock-stock.com. <br>
Mitigation: Avoid submitting sensitive watchlist or trading-interest data unless that external endpoint is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shinewilzhang/stock-clawhub) <br>
- [Publisher profile](https://clawhub.ai/user/shinewilzhang) <br>
- [Mock stock API network endpoint](https://api.mock-stock.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text and JSON from command-line stock queries, with agent-facing guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ticker symbols, ETF names, and query terms may be sent to api.mock-stock.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
