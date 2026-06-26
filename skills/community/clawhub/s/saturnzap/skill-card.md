## Description: <br>
Non-custodial Lightning wallet for AI agents via `sz` CLI: send/receive sats, pay invoices, auto-pay HTTP 402 (L402), manage channels and liquidity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shoneanstey](https://clawhub.ai/user/shoneanstey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use SaturnZap to let AI agents work with non-custodial Lightning wallets for L402 API payments, BOLT11 invoices, balance checks, channel management, and liquidity monitoring. It is not intended for custodial services, on-chain-only Bitcoin transactions, or non-Lightning crypto payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents real Lightning spending power, including on mainnet. <br>
Mitigation: Start on signet or with a low-balance wallet, use `--max-sats`, and enforce `SZ_MCP_MAX_SPEND_SATS` or `SZ_CLI_MAX_SPEND_SATS` before allowing autonomous payments. <br>
Risk: Wallet secrets or the recovery mnemonic can be exposed through chat, logs, or configuration files. <br>
Mitigation: Initialize with `--backup-to` and `--no-mnemonic-stdout`, keep `SZ_PASSPHRASE` out of chat and production `openclaw.json`, and inject secrets through an environment or secret-store path. <br>
Risk: Setup paths may run a remote installer or install a persistent systemd service. <br>
Mitigation: Review installer and service changes before running the remote install command or `sz service install`, especially on hosts that hold real funds. <br>


## Reference(s): <br>
- [SaturnZap on ClawHub](https://clawhub.ai/shoneanstey/saturnzap) <br>
- [SaturnZap GitHub Repository](https://github.com/lqwdtech/SaturnZap) <br>
- [SaturnZap Security Scenarios](https://github.com/lqwdtech/SaturnZap/blob/main/docs/security-scenarios.md) <br>
- [SaturnZap JSON Output Contracts](references/json-contracts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON command output contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `sz` binary and `SZ_PASSPHRASE`; payment workflows should use spending caps.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
