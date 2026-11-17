## Description:

Initiate payments on the SOHO Pay credit layer using EIP-712 signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amitbiswas1992](https://clawhub.ai/user/amitbiswas1992)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use SohoPay to let an agent register a wallet, check SOHO Pay credit status, initiate credit-layer USDC payments to explicit EVM merchant addresses, and repay outstanding debt on Base mainnet or Base Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured private key can authorize transactions from the wallet it controls, including on Base mainnet.

Mitigation: Use a dedicated wallet with limited funds and allowances, keep the key local, and avoid reusing a primary mainnet wallet.

Risk: Payment, registration, repayment, and approval transactions can spend gas, move USDC or credit, and may be irreversible once submitted.

Mitigation: Review the network, amount, merchant address, and contract addresses before execution; test on Base Sepolia before mainnet use.

Risk: Automated payment flows can execute high-impact actions without a wallet confirmation prompt.

Mitigation: Limit autonomous workflows, require explicit user intent for payment and repayment actions, and monitor transaction results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amitbiswas1992/skills/sohopay-1-0-15)
- [Publisher profile](https://clawhub.ai/user/amitbiswas1992)
- [Base mainnet RPC endpoint](https://mainnet.base.org)
- [Base Sepolia RPC endpoint](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status, setup guidance, command-line output, and blockchain transaction hashes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include wallet-derived addresses, credit profile values, balances, transaction hashes, and transaction status messages.]

## Skill Version(s):

1.0.15 (source: package.json, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
