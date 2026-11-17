## Description:

Portable Solana wallet operations for agents, including wallet creation, address lookup, SOL balance checks, devnet airdrops, Ed25519 message signing, signature verification, and explicit-preview RockPaperClaw deposit support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhentan](https://clawhub.ai/user/zhentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to manage a local Solana wallet for devnet or explicitly requested mainnet workflows, including address lookup, balance checks, devnet airdrops, message signing, and signature verification. It also supports previewing and, after explicit confirmation, submitting a RockPaperClaw deposit transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Solana private key files are created or loaded by the helper script.

Mitigation: Use devnet or a dedicated low-value wallet, keep keypair files secret, and set an explicit SOLANA_WALLET_KEYPAIR for sensitive actions.

Risk: The RockPaperClaw deposit command can move funds when executed.

Mitigation: Review the preview output, verify it against current RockPaperClaw deposit metadata, and rerun with --execute only after explicit approval.

Risk: Runtime dependencies are installed through npm and no lockfile is present in the artifact evidence.

Mitigation: Pin and review dependencies with a lockfile before using mainnet wallets or large balances.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhentan/skills/solana-wallet-rpc)
- [Solana Devnet RPC Endpoint](https://api.devnet.solana.com)
- [Circle Faucet](https://faucet.circle.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce structured JSON containing wallet addresses, balances, airdrop signatures, message signatures, verification results, or deposit previews.]

## Skill Version(s):

1.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
