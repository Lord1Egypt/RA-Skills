## Description: <br>
Provides real-time crypto market intelligence through MCP tools for live orderflow across 20 exchanges, directional regime detection, historical OHLCV with buy/sell flow, and on-chain address risk profiling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tunedforai](https://clawhub.ai/user/tunedforai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query live crypto market data, orderflow, macro regime signals, historical bars, and wallet address risk through a registered MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses and trading questions sent to the MCP provider may reveal identity, holdings, or trading intent. <br>
Mitigation: Only submit addresses and questions you are comfortable sharing with the provider; do not provide private keys, seed phrases, exchange logins, or other secrets. <br>
Risk: Market signals, address labels, and live data can be stale, incomplete, or unsuitable as sole input for trading decisions. <br>
Mitigation: Treat results as informational, check freshness and risk fields, and corroborate important decisions with independent sources before acting. <br>


## Reference(s): <br>
- [x402 MCP server](https://x402.tunedfor.ai/mcp) <br>
- [x402 REST API](https://x402.tunedfor.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with MCP tool-call arguments and shell command snippets; MCP tools return structured market data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote MCP endpoint; MCP access is free and rate-limited, with REST setup available through api_info().] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
