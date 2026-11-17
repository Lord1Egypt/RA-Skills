## Description:

Register agents on the Zeru ERC-8004 Identity Registry, manage wallets and metadata, and read on-chain state on Base Mainnet or Base Sepolia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elitex45](https://clawhub.ai/user/elitex45)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register AI agents in the Zeru ERC-8004 registry, inspect registration fees and agent records, and update owner-controlled metadata or wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Register, set-metadata, and unset-wallet are live on-chain actions that can cost funds or change public agent state.

Mitigation: Review each command before execution, confirm chain selection, and test on Base Sepolia before using a funded Base Mainnet wallet.

Risk: The skill handles funded wallet private keys for write operations.

Mitigation: Use a dedicated low-balance wallet key and avoid placing a primary funded key in plaintext configuration.

Risk: Reading arbitrary agent IDs may cause the runtime to request URLs chosen by other registry participants.

Mitigation: Treat fetched agent metadata as untrusted and prefer known agent IDs or an isolated runtime for inspection.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/elitex45/skills/zeruai)
- [ERC-8004 registration-v1](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)
- [OASF repository](https://github.com/agntcy/oasf/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require PRIVATE_KEY and may submit live on-chain transactions; read and fee operations can run without a private key.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
