## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obrezhniev](https://clawhub.ai/user/obrezhniev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to create and manage an agent DID, link it to a human owner, sign identity challenges, and verify DID ownership through Billions Network identity flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent identity private keys can be stored on disk without encryption when BILLIONS_NETWORK_MASTER_KMS_KEY is not set.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing keys, restrict ~/.openclaw/billions permissions, and use the encrypted storage mode for deployments.

Risk: Reusing an asset-holding Ethereum wallet key as an identity key could expand the impact of key exposure.

Mitigation: Use only a dedicated identity key that holds no assets and can be revoked or replaced.

Risk: Identity linking and signing operations depend on persistent local state and should not continue after script failures.

Mitigation: Check configured identities before signing or linking, stop on non-zero script exits, and avoid manual cryptographic workarounds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/obrezhniev/skills/the-verified-agent-identity)
- [Billions Network](https://billions.network/)
- [Billions Wallet](https://wallet.billions.network)
- [Billions Identity Dashboard](https://identity-dashboard.billions.network)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script outputs such as DID strings, JSON identity entries, verification URLs, and success or error text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and may read or write persistent identity state under ~/.openclaw/billions.]

## Skill Version(s):

1.12.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
