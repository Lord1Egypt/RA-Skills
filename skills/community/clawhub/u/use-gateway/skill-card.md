## Description: <br>
Integrate Circle Gateway to maintain unified USDC balances across supported EVM and Solana networks and perform fast crosschain transfers using deposit, burn, and mint workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Circle Gateway integrations for unified USDC balances, deposits, balance queries, and crosschain transfers across supported EVM and Solana networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can initiate real USDC transfers, wallet signatures, and contract interactions. <br>
Mitigation: Default to testnets and require explicit human review of network, recipient, amount, token, fees, and expiry before signing or broadcasting. <br>
Risk: Circle API keys, entity secrets, private keys, or signing keys may be exposed if copied into code or logs. <br>
Mitigation: Keep credentials server-side in environment variables or a secrets manager, and avoid committing or logging secret material. <br>
Risk: Incorrect Gateway contract addresses, API URLs, domain IDs, token decimals, or signing payloads can cause failed transactions or fund loss. <br>
Mitigation: Verify addresses and API URLs against Circle's official docs, use 6-decimal USDC amounts, and preserve the documented EIP-712 and Solana signing payload formats exactly. <br>
Risk: Using a raw Solana wallet address as a destination recipient can route funds incorrectly. <br>
Mitigation: Validate whether the destination is already a USDC token account before deriving or using an associated token account. <br>


## Reference(s): <br>
- [Use Gateway on ClawHub](https://clawhub.ai/mscandlen3/use-gateway) <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>
- [Gateway Contract Addresses Configuration](references/config.md) <br>
- [Depositing USDC on EVM](references/deposit-evm.md) <br>
- [Depositing USDC on EVM from a Circle Developer-Controlled Wallet](references/deposit-evm-circle-wallet.md) <br>
- [Depositing USDC on Solana](references/deposit-solana.md) <br>
- [Query Gateway Balance](references/query-balance.md) <br>
- [Gateway EVM-to-EVM Transfer Reference](references/evm-to-evm.md) <br>
- [Gateway EVM-to-Solana Transfer Reference](references/evm-to-solana.md) <br>
- [Gateway Solana-to-EVM Transfer Reference](references/solana-to-evm.md) <br>
- [Gateway Solana-to-Solana Transfer Reference](references/solana-to-solana.md) <br>
- [Transfer Gateway Balance with Circle Developer-Controlled Wallets](references/transfer-evm-circle-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, configuration, API, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow-specific examples for EVM, Solana, Circle Wallets, and Gateway API interactions.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
