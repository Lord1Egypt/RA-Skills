## Description: <br>
Check balances across Coinbase, Polymarket (Polygon USDC), Kalshi, and sportsbook accounts, providing a unified capital view with low-balance alerts while remaining read-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect current balances, total available capital, fund allocation, and low-balance conditions across supported trading and wallet platforms. It is intended for read-only balance checks and not for transfers, withdrawals, trades, or account changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles exchange API keys, API secrets, wallet addresses, and financial balance data. <br>
Mitigation: Use read-only credentials where available, provide secrets through environment variables, and avoid sharing command output that exposes sensitive account details. <br>
Risk: Users may ask the agent to move funds, place trades, or modify accounts after viewing balances. <br>
Mitigation: Keep this skill limited to read-only balance checks and route fund movement or trading requests to separately reviewed tools with appropriate security controls. <br>


## Reference(s): <br>
- [Coinbase API settings](https://www.coinbase.com/settings/api) <br>
- [AgentBets Wallet Balance Checker guide](https://agentbets.ai/guides/openclaw-wallet-balance-checker-skill/) <br>
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided read-only credentials or wallet endpoint settings for supported platforms.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
