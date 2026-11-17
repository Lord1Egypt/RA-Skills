## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[layman88](https://clawhub.ai/user/layman88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage Billions Network DIDs, link agent identities to human owners, and generate or verify cryptographic authentication proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages local identity keys and authentication proofs.

Mitigation: Install only when local identity-key management is acceptable, protect $HOME/.openclaw/billions as sensitive secret storage, and verify each signing or linking request before execution.

Risk: Private keys may be stored locally without at-rest encryption if BILLIONS_NETWORK_MASTER_KMS_KEY is not configured.

Mitigation: Set a strong BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities.

Risk: Real private keys or tokens passed on the command line can be exposed through shell history or process metadata.

Mitigation: Avoid passing real private keys or tokens on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/layman88/skills/vai-layman88)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts return DID strings, JSON entries, challenge values, verification URLs, or verification status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and can use BILLIONS_NETWORK_MASTER_KMS_KEY to encrypt local identity keys.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
