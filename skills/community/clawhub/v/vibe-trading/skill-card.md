## Description: <br>
Professional finance research toolkit for agent-assisted backtesting, factor analysis, options analysis, market data retrieval, trade-journal analysis, shadow-account research, and multi-agent investment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warren618](https://clawhub.ai/user/warren618) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, researchers, and finance-focused agent users use this skill to connect an agent to research workflows for market data, backtests, factor analysis, options analysis, trading-journal diagnostics, and generated research reports. Broker connectors, local journals, credentials, and external MCP servers should be used only when the operator trusts those inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive trading data, broker account views, OAuth profiles, local journal files, and finance credentials. <br>
Mitigation: Connect only trusted broker accounts, OAuth profiles, local journals, and external MCP servers; review optional credentials and ~/.vibe-trading configuration before use. <br>
Risk: Market data, backtests, strategy reports, and shadow-account outputs can be incomplete, stale, or unsuitable for live trading decisions. <br>
Mitigation: Treat outputs as research support, validate source data and assumptions, and review generated strategies or reports before relying on them. <br>
Risk: External MCP server configuration may extend the agent's tool surface and expose additional data paths. <br>
Mitigation: Use external MCP servers only from trusted operators, keep tool allowlists narrow, and avoid enabling session-level MCP injection unless the deployment explicitly requires it. <br>


## Reference(s): <br>
- [Vibe Trading on ClawHub](https://clawhub.ai/warren618/vibe-trading) <br>
- [Publisher profile: warren618](https://clawhub.ai/user/warren618) <br>
- [Interactive Brokers MCP API endpoint](https://api.ibkr.com/v1/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, text, JSON-like tool outputs, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce research reports, backtest metrics, generated strategy files, market-data summaries, and broker-readiness guidance depending on the invoked tool.] <br>

## Skill Version(s): <br>
0.1.10 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
