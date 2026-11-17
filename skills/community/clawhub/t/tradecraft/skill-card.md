## Description:

This skill helps agents use the Tradecraft.finance API to execute Solana token trades, manage wallets, monitor signals, and collaborate in trading groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psuede](https://clawhub.ai/user/psuede)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to equip agents with Tradecraft.finance API workflows for authenticated Solana trading, wallet operations, signal subscriptions, and trading-group interaction. It is intended for agents that have explicit account authority and appropriate human oversight for live financial actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward autonomous live trading and full-position sells using real Tradecraft account authority.

Mitigation: Require human confirmation for live buy and sell actions, especially full-position sells and trades triggered from signal polling.

Risk: High-privilege API keys can enable trading, wallet changes, signal subscriptions, and group administration.

Mitigation: Create the narrowest possible API key scopes for the intended workflow and store keys securely outside prompts and chat messages.

Risk: Wallet operations and trading-enabled wallets can expose real funds to automated decisions.

Mitigation: Use a dedicated low-balance wallet and keep autonomous signal trading disabled or gated unless a human has approved the strategy.

Risk: Portfolio data and group messages may be exposed through chat workflows or an unspecified LLM provider.

Mitigation: Avoid sending portfolio details, API keys, or private group content to chat or external model providers unless that data flow is explicitly approved.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/psuede/skills/tradecraft)
- [Tradecraft API Skill](https://tradecraft.finance/skills.md)
- [Authentication](https://tradecraft.finance/AUTH.md)
- [Trading API](https://tradecraft.finance/TRADING.md)
- [Wallets API](https://tradecraft.finance/WALLETS.md)
- [Signals API](https://tradecraft.finance/SIGNALS.md)
- [Groups API](https://tradecraft.finance/GROUPS.md)
- [Agent Heartbeat Guide](https://tradecraft.finance/HEARTBEAT.md)
- [Error Code Reference](https://tradecraft.finance/ERRORS.md)
- [Tradecraft web app](https://tradecraft.finance)
- [Tradecraft status](https://status.tradecraft.finance)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with API endpoint tables, curl examples, JSON response examples, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tradecraft API key and scoped permissions for live API use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
