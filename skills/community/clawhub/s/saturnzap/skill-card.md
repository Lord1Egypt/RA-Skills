## Description:

Non-custodial Lightning wallet for AI agents via `sz` CLI: send/receive sats, pay invoices, auto-pay HTTP 402 (L402), manage channels and liquidity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoneanstey](https://clawhub.ai/user/shoneanstey)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let agents operate a self-custodial Lightning wallet for L402 API payments, BOLT11 invoices, wallet status checks, channels, peers, and liquidity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can spend real Lightning funds through a self-custodial wallet.

Mitigation: Use testnet or signet first, keep only small balances available, and set strict `SZ_MCP_MAX_SPEND_SATS` or `SZ_CLI_MAX_SPEND_SATS` caps.

Risk: Wallet seed phrases and `SZ_PASSPHRASE` values can grant wallet access if exposed.

Mitigation: Keep mnemonics and passphrases out of chat, logs, and shared config; prefer protected secret injection or a mode-0600 environment file.

Risk: The setup path includes a one-line remote installer and an optional persistent systemd service.

Mitigation: Review installer contents, service unit behavior, environment files, firewall effects, and removal steps before enabling the service.

## Reference(s):

- [SaturnZap project homepage](https://github.com/lqwdtech/SaturnZap)
- [Security scenarios](https://github.com/lqwdtech/SaturnZap/blob/main/docs/security-scenarios.md)
- [JSON output contracts](references/json-contracts.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance expects `sz` command output to be parsed as JSON.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
