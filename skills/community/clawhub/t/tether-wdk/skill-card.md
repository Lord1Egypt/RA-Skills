## Description: <br>
Tether Wallet Development Kit (WDK) helps agents guide development of non-custodial, multi-chain wallet integrations across Bitcoin, EVM chains, Solana, Spark, TON, TRON, swaps, bridges, lending, fiat ramps, and x402 payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tether-skills](https://clawhub.ai/user/tether-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Tether WDK wallet, payment, and DeFi integrations, including package selection, chain-specific configuration, transaction flows, and safety checks for real-money operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet examples and integrations can affect real funds, and weak secret handling can expose seed phrases, signing keys, or MoonPay credentials. <br>
Mitigation: Use test wallets first, store secrets only in protected backend or secret-manager storage, avoid browser no-op sodium shims for real signing keys, and clear wallet material after use. <br>
Risk: Transaction, swap, bridge, lending, fiat, and paid x402 flows can create irreversible transfers or charges if executed without review. <br>
Mitigation: Require explicit user confirmation, quote fees and amounts before execution, validate recipients and chains, and re-confirm high-balance, new-recipient, or externally sourced requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tether-skills/tether-wdk) <br>
- [Official Tether WDK documentation](https://docs.wallet.tether.io) <br>
- [Tether WDK GitHub repository](https://github.com/tetherto/wdk) <br>
- [WDK npm package](https://www.npmjs.com/package/@tetherto/wdk) <br>
- [Chain and unit reference](references/chains.md) <br>
- [Deployments and token addresses](references/deployments.md) <br>
- [Bitcoin wallet reference](references/wallet-btc.md) <br>
- [EVM wallet reference](references/wallet-evm.md) <br>
- [Solana wallet reference](references/wallet-solana.md) <br>
- [Spark wallet reference](references/wallet-spark.md) <br>
- [TON wallet reference](references/wallet-ton.md) <br>
- [TRON wallet reference](references/wallet-tron.md) <br>
- [x402 payment reference](references/x402.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, package names, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include transaction planning guidance and must preserve explicit human confirmation before wallet write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
