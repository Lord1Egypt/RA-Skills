## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdh531916-collab](https://clawhub.ai/user/mdh531916-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage decentralized agent identities, sign identity challenges, link an agent DID to a human owner, and verify DID ownership proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and persist agent identity private keys, and local storage may be plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not configured.

Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, protect the master key, and review the local $HOME/.openclaw/billions storage location.

Risk: Passing valuable existing private keys through command-line arguments can expose sensitive material through shell history or process inspection.

Mitigation: Prefer newly generated identities or reviewed secure key-handling procedures, and avoid supplying valuable existing private keys on the command line.

Risk: DID challenge signing and human-agent linking can bind an agent identity to an owner or proof flow.

Mitigation: Review each DID, challenge, verification URL, and linking request before signing or completing the flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mdh531916-collab/skills/verified-agent-md-hasan)
- [Publisher profile](https://clawhub.ai/user/mdh531916-collab)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Node.js command examples and JSON or string command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads DID identity state under $HOME/.openclaw/billions and may emit verification URLs, DID documents, challenge strings, signature verification status, or JSON identity entries.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
