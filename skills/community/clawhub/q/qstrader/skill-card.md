## Description:

QStrader is an AI trading assistant for quantumstocks.ru that helps an agent analyze markets, check risk limits, monitor portfolios, journal trades, and execute broker actions through an n8n MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonby77](https://clawhub.ai/user/antonby77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to collect technical, LSTM, news, fundamentals, account, and position data before making broker-connected trading decisions. It also provides workflow guidance and helper scripts for pre-trade risk checks and trade journaling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is broker-connected and includes trade-opening, trade-closing, and order-modification workflows that can affect live positions.

Mitigation: Use a demo or tightly limited broker account unless the MCP server enforces authentication, per-operation authorization, and server-side confirmation for every trade.

Risk: The artifact discloses an n8n MCP trading endpoint with no authentication, and the server security summary flags weak procedural safety controls.

Mitigation: Rotate the published endpoint if it is live, require authentication before installation, and do not expose write endpoints without explicit authorization controls.

Risk: The release relies on local risk-checking logic for daily loss, margin, stop-loss, take-profit, and position-loss limits.

Mitigation: Treat local risk checks as advisory until the loss-limit logic is fixed, tested, and backed by server-side enforcement.

Risk: Setup examples source environment values and configure external services for broker, Qdrant, LightRAG, and OpenRouter access.

Mitigation: Avoid sourcing untrusted .env files, use least-privilege API keys, and rotate credentials if the environment has been shared.

## Reference(s):

- [QStrader Skill Page](https://clawhub.ai/antonby77/skills/qstrader)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [MCP Endpoints](artifact/references/mcp-endpoints.md)
- [Risk Rules](artifact/references/risk-rules.md)
- [Ticker Formats](artifact/references/ticker-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, MCP calls, configuration examples, and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured n8n MCP server with broker access; helper scripts may call mcporter, Qdrant, and market-analysis endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
