## Description: <br>
Use this skill whenever the user wants to do anything on the Yubit exchange: check prices, query wallet, spot, TradFi, earn, and perpetual futures balances, transfer funds, inspect positions and records, place or cancel perpetual futures orders, manage leverage or mode, set take-profit or stop-loss, or troubleshoot exchange requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yubit-exchange](https://clawhub.ai/user/yubit-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a Yubit exchange account through the Yubit MCP tools. It supports market data, wallet and account review, perpetual futures trading workflows, transfer workflows, and diagnostics when exchange requests fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place trades, change leverage, close positions, modify take-profit or stop-loss settings, perform batch actions, and transfer funds without an independently enforced confirmation step for every write action. <br>
Mitigation: Install only when the agent is intended to operate a live Yubit account; verify the @yubit/exchange-skill package and MCP server source, use the lowest-permission credentials available, and require explicit confirmation for every market order, leverage or mode change, position close, TP/SL change, batch action, and wallet transfer. <br>


## Reference(s): <br>
- [Yubit Exchange Skill on ClawHub](https://clawhub.ai/yubit-exchange/yubit) <br>
- [yubit-exchange Publisher Profile](https://clawhub.ai/user/yubit-exchange) <br>
- [@yubit/exchange-skill npm package](npm:@yubit/exchange-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, tool calls] <br>
**Output Format:** [Markdown guidance with Yubit MCP tool names and parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses trace IDs for diagnostics and requires read-back verification before confirming write operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
