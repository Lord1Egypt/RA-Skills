## Description:

Sage Wallet lets agents interact with the Sage Chia blockchain wallet over authenticated RPC for XCH transactions, CAT tokens, NFTs, DIDs, offers, options, coin management, and wallet configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate a Sage wallet through agent-mediated slash commands or natural language. It is intended for wallet administration, asset transfers, offer workflows, NFT and DID operations, WalletConnect signing, and network or sync monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real cryptocurrency assets through authenticated wallet RPC, including transfers, signing, offer acceptance, deletion, and database operations.

Mitigation: Use a test wallet first and require manual review of address, amount, fee, network, fingerprint, and asset identifiers before signing, broadcasting, accepting offers, deleting data, or performing database maintenance.

Risk: Remote RPC configuration can expose wallet operations to an endpoint the user does not fully trust.

Mitigation: Prefer the default local RPC endpoint and configure remote RPC only when the endpoint and certificate paths are explicitly trusted.

Risk: Mnemonic and key-management endpoints can expose or alter sensitive wallet secrets.

Mitigation: Do not request mnemonics through chat or logs, avoid plaintext storage, and treat key import, export, deletion, and mnemonic generation as high-risk operations requiring explicit user confirmation.

Risk: Some documented transaction examples use auto-submit behavior, which can sign and broadcast in one call.

Mitigation: Preview transaction details when possible and default to non-auto-submit workflows for high-value, unfamiliar, or multi-asset transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/koba42corp/skills/sage-wallet)
- [Sage RPC Endpoints Quick Reference](references/endpoints.md)
- [Sage Wallet GitHub](https://github.com/xch-dev/sage)
- [Chia Developer Documentation](https://docs.chia.net/)
- [Clawdbot Documentation](https://docs.clawd.bot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with slash commands, JSON payload examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated RPC command examples and configuration values for Sage wallet endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
