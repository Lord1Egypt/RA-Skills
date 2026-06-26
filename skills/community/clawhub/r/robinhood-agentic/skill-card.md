## Description: <br>
Connect to Robinhood Agentic Trading via MCP to view portfolios, analyze positions, place trades, and execute automated strategies through Robinhood's official MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leosaucedo](https://clawhub.ai/user/leosaucedo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an agent to Robinhood Agentic Trading for portfolio review, market-data lookup, order review, order placement, and strategy execution through the Robinhood MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants an agent sensitive financial access to Robinhood Agentic Trading. <br>
Mitigation: Install it only when that access is intentional, use a separately funded Agentic account, and revoke agent access in Robinhood settings when the environment is no longer trusted. <br>
Risk: OAuth tokens are stored locally and could be misused if the token file is exposed. <br>
Mitigation: Keep the token file protected, delete it when access is no longer needed, and rely on the documented restrictive local permissions. <br>
Risk: Trading orders can execute without an app-side confirmation prompt. <br>
Mitigation: Use Robinhood's review_equity_order MCP tool before placing orders and fund the Agentic account only with assets appropriate for agent-managed trading. <br>


## Reference(s): <br>
- [Robinhood Agentic Trading overview](https://robinhood.com/us/en/support/articles/agentic-trading-overview/) <br>
- [Robinhood trading with your agent documentation](https://robinhood.com/us/en/support/articles/trading-with-your-agent/) <br>
- [ClawHub skill page](https://clawhub.ai/leosaucedo/robinhood-agentic) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command outputs that may be plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OAuth authorization and local token storage before calling Robinhood MCP tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
