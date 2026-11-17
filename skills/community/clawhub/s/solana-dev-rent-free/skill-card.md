## Description:

Skill for Solana development using rent-free primitives from Light Protocol, covering TypeScript and Rust client development plus Anchor, native Rust, and Pinocchio program development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Solana applications with Light Protocol rent-free token accounts, mint accounts, and PDAs across DeFi, payments, airdrops, token distribution, user state, and ZK application workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm-resolved installer and referenced Lightprotocol repository contents are not pinned in the release evidence.

Mitigation: Pin the installer version and repository commit after review before using the skill in environments that can access credentials, wallet keys, or broad filesystem paths.

Risk: The skill can guide agents toward shell commands and project configuration changes for Solana development.

Mitigation: Review proposed commands and generated code before execution, especially when wallets, RPC endpoints, or production deployment settings are involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tilo-14/skills/solana-dev-rent-free)
- [Light Protocol skills repository](https://github.com/Lightprotocol/skills)
- [Light Protocol audit reports](https://github.com/Lightprotocol/light-protocol/tree/main/audits)
- [ZK Compression documentation index](https://www.zkcompression.com/llms.txt)
- [Light Token create mint guide](https://zkcompression.com/light-token/cookbook/create-mint)
- [Light Token create ATA guide](https://zkcompression.com/light-token/cookbook/create-ata)
- [Light Token transfer interface guide](https://zkcompression.com/light-token/cookbook/transfer-interface)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces development guidance and examples for agent-assisted Solana and Light Protocol workflows.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
