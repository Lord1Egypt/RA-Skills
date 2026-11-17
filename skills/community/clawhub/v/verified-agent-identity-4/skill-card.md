## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devkonten](https://clawhub.ai/user/devkonten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, manage, link, prove, and verify ownership of decentralized identities on the Billions Network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable agent identity private keys may be stored locally in plaintext by default.

Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and restrict local file access to $HOME/.openclaw/billions.

Risk: Real private keys passed on command lines may be captured by shell history or process inspection.

Mitigation: Avoid passing real private keys on command lines; use generated identities or a controlled environment when importing keys is necessary.

Risk: Generated tokens and verification URLs can grant or prove identity-related access if exposed.

Mitigation: Treat generated tokens and verification URLs as sensitive and share them only through trusted channels.

Risk: Dependency or installer drift can change the runtime behavior of identity tooling.

Mitigation: Pin installer and dependency versions in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devkonten/skills/verified-agent-identity-4)
- [Billions Network](https://billions.network/)
- [Billions Wallet](https://wallet.billions.network)
- [Billions Identity Dashboard](https://identity-dashboard.billions.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local DID, key, challenge, credential, and profile files under $HOME/.openclaw/billions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
