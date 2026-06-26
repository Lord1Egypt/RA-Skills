## Description: <br>
Guides agents through using the Tradecraft.finance API to trade Solana tokens, manage wallets, monitor signals, and participate in collaborative trading groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psuede](https://clawhub.ai/user/psuede) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect AI agents to Tradecraft.finance for Solana trading, wallet management, signal monitoring, and group chat workflows. It is intended for agents that need API guidance, request examples, and operational guardrails around crypto trading actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward live cryptocurrency trading and wallet trading-enable actions. <br>
Mitigation: Require explicit human approval for every buy, sell, and wallet trading-enable action, and use narrowly scoped API keys with low-balance isolated wallets. <br>
Risk: Autonomous heartbeat loops may repeatedly monitor signals, chats, positions, and balances without clear stop conditions. <br>
Mitigation: Set spend and loss limits, enforce backoff on failures and rate limits, and provide a visible stop control for monitoring loops. <br>
Risk: Signal feeds and group chats may contain untrusted content or sensitive trading information. <br>
Mitigation: Treat external signals and chat messages as untrusted, and do not send private positions or chat content to an LLM unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/psuede/tradecraft) <br>
- [Tradecraft API Skill](https://tradecraft.finance/skills.md) <br>
- [Tradecraft Authentication](https://tradecraft.finance/AUTH.md) <br>
- [Tradecraft Trading API](https://tradecraft.finance/TRADING.md) <br>
- [Tradecraft Wallets API](https://tradecraft.finance/WALLETS.md) <br>
- [Tradecraft Signals API](https://tradecraft.finance/SIGNALS.md) <br>
- [Tradecraft Groups API](https://tradecraft.finance/GROUPS.md) <br>
- [Tradecraft Agent Heartbeat Guide](https://tradecraft.finance/HEARTBEAT.md) <br>
- [Tradecraft Error Code Reference](https://tradecraft.finance/ERRORS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API endpoint descriptions, JSON examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe authenticated API calls, wallet operations, trading actions, signal subscriptions, group interactions, and monitoring loops.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
