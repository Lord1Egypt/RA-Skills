## Description: <br>
Create and manage AI-powered trading bots via natural language, including paper and live trading, portfolio monitoring, backtesting, stock quotes, and options chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etbars](https://clawhub.ai/user/etbars) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to create, monitor, backtest, and manage AI-powered trading bots, portfolio information, quotes, options data, and trading actions from natural-language chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose live trading and account-changing authority, including order placement, position closing, mode switching, and bot deletion. <br>
Mitigation: Use paper mode first, require explicit human confirmation for live orders and destructive actions, and configure broker-side limits before enabling live trading. <br>
Risk: A leaked or over-privileged VIBETRADER_API_KEY could allow unauthorized trading or account access. <br>
Mitigation: Use the narrowest available API key scope, store it only in the OpenClaw environment configuration, revoke it if exposed, and rotate it regularly. <br>


## Reference(s): <br>
- [VibeTrader Website](https://vibetrader.markets) <br>
- [VibeTrader Documentation](https://vibetrader.markets/docs) <br>
- [VibeTrader MCP Server](https://vibetrader-mcp-289016366682.us-central1.run.app/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/etbars/vibetrader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and natural-language responses with inline JSON, shell commands, configuration snippets, and API-backed trading or market-data results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIBETRADER_API_KEY; supports paper and live trading modes through the VibeTrader MCP server and REST API.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
