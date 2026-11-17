## Description:

QFC blockchain interaction: wallet, faucet, chain queries, staking, epoch and finality, and AI inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lai3d](https://clawhub.ai/user/lai3d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate QFC wallets, inspect chain state, interact with staking, tokens, NFTs, DeFi contracts, and submit AI inference tasks through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet secrets and irreversible blockchain transactions.

Mitigation: Use it only on a trusted machine, prefer testnet, use strong unique keystore passwords, and require explicit human confirmation before transfers, approvals, swaps, marketplace purchases, deployments, or session-key actions.

Risk: Mainnet keys, approvals, recipients, amounts, contract addresses, and explorer submissions can put funds or deployed assets at risk if accepted without review.

Mitigation: Do not use real mainnet keys until prompts, transaction parameters, contract addresses, allowances, and dependency installation paths have been reviewed and verified.

Risk: Agent and inference workflows can spend deposits through session keys within configured limits.

Mitigation: Verify permissions, daily limits, per-transaction limits, deposit balances, session-key validity, and fee estimates before submitting agent or inference actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lai3d/skills/qfc)
- [QFC Chain Overview](references/qfc-chain-overview.md)
- [QFC Wallet Operations Guide](references/wallet-operations.md)
- [ERC-20 Token Deployment on QFC](references/token-deployment.md)
- [QFC DeFi Operations Guide](references/defi-operations.md)
- [QFC AI Compute Network Guide](references/ai-compute.md)
- [QFC Governance Guide](references/governance.md)
- [QFC Error Handling Reference](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets, command examples, and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide wallet, contract, token, DeFi, marketplace, and inference operations; transaction-producing actions require review before execution.]

## Skill Version(s):

3.4.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
