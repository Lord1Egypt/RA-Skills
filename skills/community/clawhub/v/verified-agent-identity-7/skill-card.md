## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[armanma0100](https://clawhub.ai/user/armanma0100)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to create and manage Billions Network decentralized identities, sign and verify challenges, and link agent DIDs to human owners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and uses long-lived DID signing keys that can be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set.

Mitigation: Set a strong, random BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and protect $HOME/.openclaw/billions with restrictive permissions.

Risk: Signing challenges or linking identities can bind an agent identity to a human owner or prove control of a DID.

Mitigation: Require explicit confirmation before signing challenges or linking identities, and use the documented identity-check flow before running signing scripts.

Risk: Production use depends on Node.js packages and network services used for DID, attestation, and wallet flows.

Mitigation: Review, update, or pin dependencies before production use and deploy only where Billions Network and DID resolver calls are acceptable.

## Reference(s):

- [Verified Agent Identity on ClawHub](https://clawhub.ai/armanma0100/skills/verified-agent-identity-7)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local identity, key, challenge, credential, and profile files under $HOME/.openclaw/billions.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
