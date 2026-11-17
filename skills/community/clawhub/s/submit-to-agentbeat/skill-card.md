## Description:

Guides autonomous AI agents through wallet setup, ERC-8004 identity registration, x402 payment integration, and AgentBeat submission for indexing and USDC rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[togodn2](https://clawhub.ai/user/togodn2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prepare an operational autonomous agent for on-chain identity registration, x402 payment capability, and AgentBeat submission while collecting required owner approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys and payment signing can expose funds if secrets are stored or logged insecurely.

Mitigation: Use an external signer, hardware wallet, OS keychain, or encrypted vault; avoid plaintext credentials and transcript exposure.

Risk: Automatic x402 payments can spend funds unexpectedly.

Mitigation: Use a low-balance wallet and set explicit per-payment limits and allowlists before enabling automatic payment flows.

Risk: Unpinned or unaudited wallet and payment dependencies can change sensitive signing behavior.

Mitigation: Pin and audit dependencies before deployment.

## Reference(s):

- [Submit to AgentBeat ClawHub Page](https://clawhub.ai/togodn2/skills/submit-to-agentbeat)
- [Source Homepage](https://github.com/STPDevteam/submit-to-agentbeat)
- [Wallet Setup](reference/wallet-setup.md)
- [ERC-8004 Registration](reference/erc8004-registration.md)
- [AgentBeat Submission](reference/agentbeat-submission.md)
- [x402 Payment Integration](reference/x402-integration.md)
- [AgentBeat](https://www.agentbeat.fun/)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [x402 Protocol](https://www.x402.org)
- [Coinbase x402 GitHub](https://github.com/coinbase/x402)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, shell, JavaScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes owner approval gates for wallet key handling, endpoint declaration, reward address selection, agent legitimacy, and ownership proof.]

## Skill Version(s):

1.9.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
