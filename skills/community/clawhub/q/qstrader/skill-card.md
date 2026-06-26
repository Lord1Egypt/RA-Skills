## Description: <br>
AI Trading Assistant for quantumstocks.ru that supports market analysis, risk management, portfolio monitoring, trade journaling, and broker-connected trade execution through n8n MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonby77](https://clawhub.ai/user/antonby77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and finance-focused agents use this skill to analyze markets, check account and risk constraints, prepare trade theses, request user approval, and log trading decisions. It is intended for environments where the operator intentionally connects the agent to broker-capable n8n MCP infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for broker-connected trading workflows with account access and order, change, and close actions. <br>
Mitigation: Install only when broker-capable infrastructure is intended; use a private authenticated MCP endpoint, begin with paper trading, and require separate explicit user approval for every order, change, or close action. <br>
Risk: Trading setup and logging can expose credentials, account data, or trade history if environment files and logs are not controlled. <br>
Mitigation: Review the .env file before setup, limit access to secrets and logs, and avoid storing raw account data unless retention and access controls are in place. <br>
Risk: Weak scoping around live trading tools can let analysis, risk checks, and trade execution run in the same agent workflow. <br>
Mitigation: Keep read-only analysis separate from write-capable broker actions, enforce stop-loss, take-profit, margin, and daily-loss checks before any proposed trade, and reject orders that fail those checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/antonby77/qstrader) <br>
- [MCP endpoint reference](references/mcp-endpoints.md) <br>
- [Risk management rules](references/risk-rules.md) <br>
- [Ticker format reference](references/ticker-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, MCP calls, and Python helper-script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include broker-action proposals and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
