## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ch4812](https://clawhub.ai/user/ch4812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage Billions Network decentralized identities for agents, link agent DIDs to human owners, sign challenges, and verify DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and stores reusable identity private keys for agent DIDs.

Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities and restrict access to $HOME/.openclaw/billions.

Risk: Private keys can be passed on the command line when creating an identity from an existing key.

Mitigation: Avoid command-line private key arguments for real identities because shell history and process inspection can expose them.

Risk: Signing challenges and linking human-agent identities can create externally verifiable identity relationships.

Mitigation: Require explicit human approval before running signing or linking commands and stop on any script failure.

## Reference(s):

- [Billions Network](https://billions.network/)
- [ClawHub skill page](https://clawhub.ai/ch4812/skills/verified-agent-identity-new)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, DID strings, signatures, and verification URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and may persist identity state under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
