## Description:

Integrate Circle Gateway to hold a unified USDC balance across multiple blockchains and transfer USDC instantly (<500ms) via permissionless deposit, burn, and mint workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Circle Gateway deposits, balance checks, and cross-chain USDC transfers across supported EVM chains and Solana. It is intended for applications that need chain-agnostic balances, low-latency transfers, payment routing, or cross-chain capital efficiency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples can sign and submit real USDC transfers.

Mitigation: Keep workflows on testnet until explicit confirmation screens, amount/address/domain validation, and mainnet acknowledgments are in place.

Risk: A mainnet/testnet configuration mismatch is reported by security evidence.

Mitigation: Review chain configuration before deployment and verify every environment, contract address, domain ID, and Gateway API endpoint before enabling transfers.

Risk: Circle API keys and entity secrets authorize sensitive wallet operations.

Mitigation: Store credentials only in environment variables or a secrets manager, never commit or log them, and restrict production signing authority.

## Reference(s):

- [Gateway Contract Addresses Configuration](references/config.md)
- [Depositing USDC on EVM from a Circle Developer-Controlled Wallet](references/deposit-evm-circle-wallet.md)
- [Depositing USDC on EVM](references/deposit-evm.md)
- [Depositing USDC on Solana](references/deposit-solana.md)
- [Gateway EVM-to-EVM Transfers](references/evm-to-evm.md)
- [Gateway EVM-to-Solana Transfer Reference](references/evm-to-solana.md)
- [Querying Unified Balance](references/query-balance.md)
- [Gateway Solana-to-EVM Transfers](references/solana-to-evm.md)
- [Gateway Solana-to-Solana Transfer](references/solana-to-solana.md)
- [Transfer Gateway Balance via Circle Developer-Controlled Wallets](references/transfer-evm-circle-wallet.md)
- [Circle Developer Docs](https://developers.circle.com/llms.txt)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown with TypeScript, TSX, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include runnable blockchain transaction examples that require explicit user confirmation, strict validation, testnet defaults, and protected Circle credentials.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
