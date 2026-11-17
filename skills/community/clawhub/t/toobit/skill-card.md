## Description:

Trade crypto on Toobit through natural language, including spot and USDT-M futures trading, market data queries, and wallet management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxizhen](https://clawhub.ai/user/xuxizhen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Toobit market, account, wallet, spot, and USDT-M futures information and to prepare or execute Toobit trading actions through agent-generated API calls. It is intended for users who explicitly want an agent to operate a Toobit account with their API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a real Toobit account, including placing orders, canceling orders, changing futures settings, transferring assets, and withdrawing funds.

Mitigation: Install only when agent access to the Toobit account is intended, use minimum-permission API keys, and avoid withdrawal permission unless it is required.

Risk: Confirmed write actions can create financial exposure or move funds.

Mitigation: Carefully review every confirmation prompt for orders, cancellations, leverage, transfers, and withdrawals before approving.

Risk: Withdrawal capability can transfer assets out of the account.

Mitigation: Require explicit confirmation and verify the asset, quantity, destination address, and chain before approving any withdrawal.

## Reference(s):

- [Toobit API base endpoint](https://api.toobit.com)
- [ClawHub skill page](https://clawhub.ai/xuxizhen/skills/toobit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown responses with inline bash commands, API request details, confirmation prompts, and readable summaries of JSON API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signed requests require TOOBIT_API_KEY and TOOBIT_API_SECRET; write operations should present parameters and wait for user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
