## Description:

Streams live PumpFun token data on Solana with USD OHLC prices, USD volume, moving averages, and tick-to-tick percentage change from the Bitquery GraphQL WebSocket API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyn](https://clawhub.ai/user/divyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-tool builders use this skill to connect an agent to a real-time PumpFun/Solana USD price feed for dashboards, alerts, and market monitoring. The emitted trading signals should be treated as informational heuristics, not instructions to buy or sell.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bitquery API key is passed in the WebSocket URL and can be exposed through logs, shell history, proxy logs, or IDE output.

Mitigation: Run in an isolated environment, keep BITQUERY_API_KEY in the environment, avoid printing full connection URLs, monitor logs and shell history, and rotate the key if exposure is suspected.

Risk: The skill depends on a live external WebSocket API and a Python WebSocket dependency.

Mitigation: Review and pin dependencies where appropriate, test behavior in a virtualenv or container, and handle connection errors or unavailable market data before relying on the stream.

Risk: Derived trading signals can be mistaken for financial instructions.

Mitigation: Present price, volume, and signal hints as informational market data only, and require human review before any trading action.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/divyn/skills/pumpfun-usd-price-stream)
- [Bitquery Trading.Tokens PumpFun GraphQL Field Reference](references/graphql-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python code blocks, plus streaming terminal text from the included Python script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and the gql[websockets] Python dependency; connects to Bitquery over WebSocket for 1-second PumpFun token ticks on Solana.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
