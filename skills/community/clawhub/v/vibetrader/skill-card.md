## Description:

Create and manage AI-powered trading bots via natural language. Paper & live trading, portfolio monitoring, backtesting, stock quotes, and options chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etbars](https://clawhub.ai/user/etbars)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create and manage AI-powered trading bots, monitor portfolios, query market data, and run backtests through natural-language OpenClaw interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Natural-language trading actions through the remote service can affect real funds when live trading is enabled.

Mitigation: Use paper trading or read-only credentials when possible, verify API key scope, and require explicit user confirmation before live orders, live-mode switches, position closures, or bot deletion.

Risk: The skill requires a VibeTrader API key that may grant access to account, portfolio, and trading operations.

Mitigation: Install only after trusting the VibeTrader service, store the key in the configured environment variable, and avoid sharing credentials in prompts or logs.

## Reference(s):

- [VibeTrader Website](https://vibetrader.markets)
- [VibeTrader Documentation](https://vibetrader.markets/docs)
- [VibeTrader MCP Server](https://vibetrader-mcp-289016366682.us-central1.run.app/mcp)
- [VibeTrader REST API Base URL](https://vibetrader-mcp-289016366682.us-central1.run.app)
- [ClawHub Skill Page](https://clawhub.ai/etbars/skills/vibetrader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with JSON configuration, shell command examples, and REST or MCP API call descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIBETRADER_API_KEY; paper trading is documented as the default, while live trading can affect real funds.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
