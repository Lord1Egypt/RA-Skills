## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilhant-34](https://clawhub.ai/user/ilhant-34)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and external users use this skill to create and manage decentralized agent identities, link an agent DID to a human owner, sign challenges, and verify DID ownership proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent DID private keys may be stored locally in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing an identity, run the skill in an isolated account or environment, and protect $HOME/.openclaw/billions.

Risk: Old signed challenge tokens may remain reusable because challenge storage does not enforce expiration or consumption after verification.

Mitigation: Use only fresh challenges for verification and update the implementation or operating process to expire and consume challenges after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilhant-34/skills/v-identity-ilhant34)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON or text command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local identity files under $HOME/.openclaw/billions and may call Billions Network or Privado DID endpoints.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json reports 1.0.5 and artifact _meta.json reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
