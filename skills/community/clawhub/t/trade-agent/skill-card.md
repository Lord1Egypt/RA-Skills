## Description:

Manage AIUSD trading and accounts by querying balances, executing trades, staking, withdrawing, topping up gas, and viewing transaction history via MCP backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:


## Use Case:

External users and bot operators use this skill to manage AIUSD balances, trades, staking, withdrawals, gas top-ups, deposits, and transaction history through a personal assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate trades, staking, withdrawals, gas top-ups, and other account-level fund actions.

Mitigation: Require explicit human confirmation before any fund-moving action and verify destination, asset, amount, and network before execution.

Risk: The installer and reauthentication flows perform local actions that affect dependencies and authentication state.

Mitigation: Install in a dedicated directory, avoid administrator privileges, inspect the extracted package before use, and confirm with the user before reauthentication.

Risk: The reauthentication flow can delete local auth caches and generic auth files in the user's home directory.

Mitigation: Warn the user before reauthentication and preserve any needed credentials or sessions before cache removal.

Risk: Direct deposits are documented as USDC-only.

Mitigation: Confirm the asset before deposit guidance and direct non-USDC deposits to the official AIUSD website.

## Reference(s):

- [ClawHub trade-agent listing](https://clawhub.ai/chaunceyliu/skills/trade-agent)
- [AIUSD official website](https://aiusd.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce account, trading, staking, withdrawal, gas, deposit, authentication, and transaction-history guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-02-07T01:06:26Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
