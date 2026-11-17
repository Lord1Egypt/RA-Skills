## Description:

SolClaw helps agents send, receive, and monitor non-custodial USDC payments on Solana Devnet using agent names instead of wallet addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sterdam](https://clawhub.ai/user/sterdam)

### License/Terms of Use:


## Use Case:

External developers and agent operators use SolClaw to register payable agents, check balances, send or receive USDC, manage subscriptions and allowances, create invoices, and monitor payment health on Solana Devnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-sensitive commands can expose private keys or key material.

Mitigation: Use devnet-only wallets, avoid pasting real private keys into shell commands, and do not use quiet key export unless the output channel is fully controlled.

Risk: Unpinned CLI execution can run an unexpected package version.

Mitigation: Pin and verify the CLI package before running payment or wallet commands.

Risk: Automated heartbeat monitoring can expose operational payment data in logs.

Mitigation: Treat heartbeat cron jobs and log files as sensitive data and restrict access to their output.

Risk: The skill operates payment flows on Solana Devnet and may be mistaken for mainnet-ready financial infrastructure.

Mitigation: Confirm network configuration before use and limit activity to devnet-only assets unless the release evidence explicitly supports another network.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sterdam/skills/solclaw)
- [SolClaw skill definition](https://solclaw.xyz/skill.md)
- [SolClaw heartbeat routine](https://solclaw.xyz/heartbeat.md)
- [SolClaw API health endpoint](https://solclaw.xyz/api/health)
- [Solana Devnet explorer](https://explorer.solana.com/?cluster=devnet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with shell command examples and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet-sensitive guidance for Solana Devnet payments and monitoring.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
