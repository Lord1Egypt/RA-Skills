## Description:

Tether Wallet Development Kit (WDK) helps developers build non-custodial multi-chain wallets and integrations for wallet creation, transactions, token transfers, DEX swaps, cross-chain bridges, DeFi lending/borrowing, fiat on/off ramps, and x402 payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tether-skills](https://clawhub.ai/user/tether-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build agent-assisted wallet integrations with Tether WDK across Bitcoin, EVM, Solana, Spark, TON, and TRON. It supports wallet setup, balance and fee queries, transaction preparation, token transfers, swaps, bridges, lending workflows, fiat on/off ramps, and x402 payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signing, transaction, and x402 payment flows can move real funds or authorize irreversible actions.

Mitigation: Require explicit user confirmation, quote fees before writes, use payment allowlists, and keep facilitator wallets isolated and low-balance.

Risk: Wallet seeds, mnemonics, key material, MoonPay credentials, and TON credentials could be exposed in frontend code, logs, repositories, or agent output.

Mitigation: Keep secrets out of frontend bundles and logs, avoid printing key material, and use read-only accounts for balance and fee queries.

Risk: Dependency or package drift could change wallet behavior or introduce unsafe transitive code.

Mitigation: Pin and review dependencies, verify package versions before adding them, and scan updates before funded-wallet use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tether-skills/skills/tether-wdk)
- [Publisher profile](https://clawhub.ai/user/tether-skills)
- [Tether WDK documentation](https://docs.wallet.tether.io)
- [Tether WDK GitHub repository](https://github.com/tetherto/wdk)
- [WDK package](https://www.npmjs.com/package/@tetherto/wdk)
- [Chain and unit reference](references/chains.md)
- [Deployments reference](references/deployments.md)
- [Bitcoin wallet reference](references/wallet-btc.md)
- [EVM wallet reference](references/wallet-evm.md)
- [Solana wallet reference](references/wallet-solana.md)
- [Spark wallet reference](references/wallet-spark.md)
- [TON wallet reference](references/wallet-ton.md)
- [TRON wallet reference](references/wallet-tron.md)
- [Swap protocol reference](references/protocol-swap.md)
- [Bridge protocol reference](references/protocol-bridge.md)
- [Lending protocol reference](references/protocol-lending.md)
- [Fiat protocol reference](references/protocol-fiat.md)
- [x402 payment reference](references/x402.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces developer guidance and code/configuration examples; it should not execute wallet transactions by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
