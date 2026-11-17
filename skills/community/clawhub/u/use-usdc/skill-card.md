## Description:

Helps agents work with Circle USDC across EVM chains and Solana by checking balances, preparing transfers, approving EVM spending, and verifying transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to produce USDC integration guidance and transaction code for EVM and Solana workflows. It is most relevant for balance checks, payment transfers, EVM approvals, token address lookup, and transaction verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw private keys may be exposed or misused when following wallet setup examples.

Mitigation: Use low-value or test wallets by default, and prefer a hardware signer, encrypted secret store, scoped signing service, or safer wallet flow before using mainnet funds.

Risk: Generated code installs unpinned blockchain packages for workflows involving financial transactions.

Mitigation: Pin dependency versions, review packages before execution, and run generated code in a controlled development environment.

Risk: Wrong recipient, chain, amount, token contract, mint, or approval can cause irreversible loss or unintended spending authority.

Mitigation: Require explicit confirmation for write transactions and independently verify recipient, chain ID, amount, USDC contract or mint, approval spender, and transaction receipt before reporting success.

## Reference(s):

- [EVM Operations Guide](references/evm.md)
- [Solana Operations Guide](references/solana.md)
- [Circle USDC Contract Addresses](https://developers.circle.com/stablecoins/usdc-contract-addresses)
- [Circle Developers](https://developers.circle.com)
- [Circle Faucet](https://faucet.circle.com)
- [Solana Faucet](https://faucet.solana.com)
- [Viem Documentation](https://viem.sh)
- [Circle Stablecoin EVM Contracts](https://github.com/circlefin/stablecoin-evm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include blockchain transaction previews, dependency installation commands, contract or mint addresses, and verification steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
