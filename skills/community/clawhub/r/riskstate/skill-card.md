## Description: <br>
Pre-trade risk API for crypto trading agents that returns exposure limits, allowed actions, and policy constraints for BTC/USD and ETH/USD from 30+ real-time signals across spot, perpetual futures, and DeFi borrowing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likidodefi](https://clawhub.ai/user/likidodefi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, trading-system operators, and capital desks use this skill to query RiskState before opening, sizing, or maintaining BTC/USD and ETH/USD exposure. Agents use the returned policy fields to enforce position limits, leverage caps, blocked actions, and DeFi health constraints before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends RiskState API keys, requested assets, and optional wallet addresses to RiskState's external service. <br>
Mitigation: Use a scoped API key stored in environment variables or a secret manager, and provide a wallet address only when DeFi analysis is needed. <br>
Risk: Risk output depends on live external market and DeFi data, which may be stale, degraded, unavailable, or rate-limited. <br>
Mitigation: Follow the documented failure-mode behavior: treat stale or low-quality data as degraded, abstain when data quality is unreliable, and fail closed on timeouts or server errors. <br>
Risk: The optional MCP server is a separate integration path from the skill files reviewed here. <br>
Mitigation: Review and scan the optional MCP server independently before installing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/likidodefi/riskstate) <br>
- [RiskState homepage](https://riskstate.ai) <br>
- [RiskState API documentation](https://riskstate.ai/docs/api) <br>
- [RiskState API v1 reference](docs/api-v1.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, JSON] <br>
**Output Format:** [Markdown guidance with curl examples, integration snippets, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RiskState bearer token; optional wallet address enables DeFi position analysis.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
