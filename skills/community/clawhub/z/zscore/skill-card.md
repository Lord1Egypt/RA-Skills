## Description:

Register agents on the Zeru ERC-8004 Identity Registry, manage wallets and metadata, and read on-chain state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elitex45](https://clawhub.ai/user/elitex45)

### License/Terms of Use:


## Use Case:

Developers and agent operators use zscore to register agents on the Zeru ERC-8004 Identity Registry, check registry fees, read agent state, and manage agent metadata or wallet settings on Base Mainnet or Base Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write commands can use a funded private key to submit irreversible on-chain transactions.

Mitigation: Use a dedicated low-balance wallet, prefer Base Sepolia for testing, and review each write command before execution.

Risk: Reading unknown agent IDs can fetch metadata from untrusted URLs.

Mitigation: Treat fetched metadata as untrusted and avoid reading unknown IDs from environments where outbound requests are sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elitex45/skills/zscore)
- [ERC-8004 registration-v1 reference](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)
- [OASF reference](https://github.com/agntcy/oasf/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands require node, npx, and a PRIVATE_KEY; write operations can submit blockchain transactions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
