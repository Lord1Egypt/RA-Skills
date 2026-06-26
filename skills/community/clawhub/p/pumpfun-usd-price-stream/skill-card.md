## Description: <br>
Streams real-time PumpFun token price data on Solana from Bitquery over WebSocket, including USD OHLC, volume, moving averages, and tick-to-tick percentage changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Divyn](https://clawhub.ai/user/Divyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-tool builders use this skill to add a live PumpFun/Solana market-data feed to agents, dashboards, or alerting workflows. It helps inspect USD prices, volume, moving averages, and short-interval changes for tokens whose Solana address includes pump. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required Bitquery API key is passed in the WebSocket URL and may be exposed through logs, shell history, proxy logs, or shared debugging output. <br>
Mitigation: Store the key only in an environment variable, avoid printing or logging the full WebSocket URL, monitor likely log locations, and rotate the key if exposure is suspected. <br>
Risk: The skill opens a WebSocket connection to Bitquery and depends on the Python gql websockets package. <br>
Mitigation: Run it in an isolated environment such as a virtualenv or container, review network egress expectations, and pin the dependency before production use. <br>
Risk: Live PumpFun token data and derived signal hints can be volatile, intermittent, or incomplete for trading decisions. <br>
Mitigation: Validate the feed and any alert logic against independent checks before acting on it, and treat generated signal hints as operational data rather than financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Divyn/pumpfun-usd-price-stream) <br>
- [Bitquery Trading.Tokens PumpFun field reference](references/graphql-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; runtime script prints formatted text ticks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and WebSocket access to Bitquery; live market data and derived signal hints should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
