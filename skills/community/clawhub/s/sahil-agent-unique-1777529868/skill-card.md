## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sahilkhan6006](https://clawhub.ai/user/sahilkhan6006)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to create and manage Billions Network DIDs, link an agent identity to a human owner, and generate or verify signed identity challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or imports agent identity private keys and may persist them in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not configured.

Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities, protect $HOME/.openclaw/billions as sensitive storage, and avoid using valuable wallet keys with --key.

Risk: Generated verification links, signed challenges, and tokens can act as authentication material.

Mitigation: Share links and tokens only with the intended verifier, review requests before signing, and regenerate challenges when a request is stale or exposed.

Risk: The skill relies on npm dependencies and network-facing identity services for DID, attestation, and verification workflows.

Mitigation: Review or update dependencies before production use and confirm the configured Billions and resolver endpoints are acceptable for the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sahilkhan6006/skills/sahil-agent-unique-1777529868)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist DID identity records, challenges, credentials, and key material under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
