## Description: <br>
AI-powered perpetual futures trading on Hyperliquid DEX that handles account creation, USDC onboarding, vault management, and autonomous trade execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shekel-xyz](https://clawhub.ai/user/shekel-xyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create and manage Hyperliquid perpetual futures trading accounts, configure strategy and risk limits, execute trades, manage USDC deposits and withdrawals, and operate Hyperliquid vaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over a crypto trading account through a powerful API key. <br>
Mitigation: Use a proper secret manager or enter the key only when needed; do not store the API key in agent memory. <br>
Risk: Autonomous trading, scheduled runs, and vault operations can move real funds and create financial loss. <br>
Mitigation: Fund minimally, set strict risk limits such as maximum open positions, daily loss, and drawdown thresholds, and review trading settings before enabling schedules. <br>
Risk: Withdrawal, vault, wallet-key export, and account deletion actions are high-impact account operations. <br>
Mitigation: Require explicit user confirmation before withdrawals, vault actions, wallet-key export, account deletion, and scheduled trading changes. <br>
Risk: Remote skill instructions may change over time. <br>
Mitigation: Review remote instruction changes before allowing the agent to act on updated instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shekel-xyz/shekel-hyperliquid) <br>
- [Shekel Skill Service](https://shekel-skill-backend.onrender.com/skill) <br>
- [Shekel Dashboard](https://www.shekel.xyz/hl-skill-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHEKEL_API_KEY for authenticated account, trading, withdrawal, vault, and key-management actions.] <br>

## Skill Version(s): <br>
1.14.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
