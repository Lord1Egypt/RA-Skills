## Description:

Verified Agent Identity helps agents create and manage Billions decentralized identities, link them to human owners through Billions ERC-8004 and Attestation Registries, and verify authentication proofs using iden3-based workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamlucker21](https://clawhub.ai/user/adamlucker21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create local DID identities, link an agent identity to a human owner, sign identity challenges, and verify signed challenges for DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local DID private keys may be created or stored in ways that expose sensitive identity material.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and use the skill only when local DID key storage is acceptable.

Risk: Supplying private keys through command-line arguments can expose them through shell history or process inspection.

Mitigation: Avoid importing private keys through command-line arguments.

Risk: Signing challenges or linking an agent identity to a person can create identity assertions with insufficient confirmation.

Mitigation: Require explicit user confirmation before signing challenges or linking an agent identity to a person.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adamlucker21/skills/verified-agent-identity-6)
- [Billions Network](https://billions.network/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to run Node.js scripts that create DIDs, sign challenges, link agent and human identities, or verify signatures.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
