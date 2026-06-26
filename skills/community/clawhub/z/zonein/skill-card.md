## Description: <br>
Autonomous Hyperliquid trading agent for smart-money signals, market analysis, backtesting, and live trading-agent workflows across Hyperliquid and Polymarket data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phutt-bwai](https://clawhub.ai/user/phutt-bwai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill to inspect smart-money signals, configure Hyperliquid trading agents, manage HITL trade plans, and run approved trading or account-management commands through a Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real-money automated trading. <br>
Mitigation: Install only when that authority is intended; prefer HITL mode, set loss limits and withdrawal whitelists, and review every command before approval. <br>
Risk: Some state-changing commands do not have a programmatic confirmation gate. <br>
Mitigation: Use explicit human approval before agent-update, agent-delete, telegram-disable, or similar state changes, and avoid batching unrelated changes. <br>
Risk: Secret-handling gaps could expose API keys or Telegram bot tokens in shared logs or transcripts. <br>
Mitigation: Use dedicated revocable keys, avoid pasting tokens into shared contexts, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phutt-bwai/zonein) <br>
- [Publisher profile](https://clawhub.ai/user/phutt-bwai) <br>
- [ZoneIn homepage](https://zonein.xyz) <br>
- [ZoneIn app](https://app.zonein.xyz) <br>
- [ZoneIn API docs](https://mcp.zonein.xyz/docs) <br>
- [Commands reference](references/COMMANDS.md) <br>
- [Data sources reference](references/DATA_SOURCES.md) <br>
- [Agent configuration reference](references/AGENT_CONFIG.md) <br>
- [Trigger conditions reference](references/TRIGGER_CONDITIONS.md) <br>
- [Workflows reference](references/WORKFLOWS.md) <br>
- [API response schema](references/schema.md) <br>
- [Strategy reference](references/strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-derived summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit executable Python CLI commands for read-only, state-changing, and user-confirmed financial actions.] <br>

## Skill Version(s): <br>
2.3.8 (source: server release metadata; artifact frontmatter reports 2.3.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
