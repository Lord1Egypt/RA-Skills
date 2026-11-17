## Description:

Check balances across Coinbase, Polymarket (Polygon USDC), Kalshi, and sportsbook accounts, providing a unified capital view with low-balance alerts while remaining read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check available balances, total capital, fund allocation, and low-balance status across supported financial accounts. The artifact includes a Coinbase balance query and states that the skill must not transfer funds, place trades, modify account settings, or send funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests multiple financial account credentials and wallet-related environment variables.

Mitigation: Use read-only, least-privilege API keys; run the skill only on trusted machines; and avoid sharing credentials in prompts, logs, or shared terminals.

Risk: Security evidence says the skill asks for Kalshi, Polygon, and Polymarket credentials that its current instructions do not actually use.

Mitigation: Provide only the Coinbase credentials needed for the evidenced balance check unless additional account checks are documented and reviewed.

Risk: Security evidence flags Coinbase credential handling as needing review before installation.

Mitigation: Review the generated Coinbase request and signature handling before execution, and rotate credentials if they may have been exposed.

## Reference(s):

- [Wallet Balance Checker Skill Page](https://clawhub.ai/rsquaredsolutions2026/skills/wallet-balance-checker)
- [Coinbase API Settings](https://www.coinbase.com/settings/api)
- [AgentBets Wallet Balance Checker Tutorial](https://agentbets.ai/guides/openclaw-wallet-balance-checker-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash snippets and JSON balance summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq. Uses read-only financial API credentials, a Polygon RPC URL, and a Polymarket wallet address when relevant.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
