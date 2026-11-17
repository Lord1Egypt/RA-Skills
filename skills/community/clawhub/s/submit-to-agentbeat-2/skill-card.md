## Description:

Complete submission flow for autonomous AI agents into the on-chain agent economy, including EVM wallet setup, owner gas funding, ERC-8004 identity registration, x402 payment capability, and AgentBeat submission for indexing and USDC rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nugdw](https://clawhub.ai/user/nugdw)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to prepare an autonomous agent for AgentBeat by creating or locating an EVM wallet, registering an ERC-8004 identity, configuring x402 payments, and submitting the profile for indexing and rewards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may give an agent authority over private keys and persistent wallet data.

Mitigation: Use an external signer, hardware wallet, OS keychain, or encrypted vault; do not paste or log private keys; avoid local plaintext storage unless the owner explicitly approves it.

Risk: The workflow can initiate payments, on-chain transactions, and reward-address decisions.

Mitigation: Require explicit owner approval for every transaction, payment destination, reward address, and fallback to an x402 payment address.

Risk: AgentBeat vouchers and wallet details can be sensitive if shared publicly.

Mitigation: Treat vouchers as secrets and require owner approval before any public post or external disclosure involving wallet or voucher data.

Risk: Unpinned package installation may introduce dependency risk.

Mitigation: Pin and review dependencies before installing x402, EVM, or wallet-related packages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nugdw/skills/submit-to-agentbeat-2)
- [AgentBeat Submission](reference/agentbeat-submission.md)
- [ERC-8004 Registration](reference/erc8004-registration.md)
- [Wallet Setup](reference/wallet-setup.md)
- [x402 Payment Integration](reference/x402-integration.md)
- [AgentBeat](https://www.agentbeat.fun/)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hard owner-approval gates for key handling, endpoint declaration, reward address selection, on-chain actions, and voucher sharing.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.8.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
