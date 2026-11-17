## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holdcc](https://clawhub.ai/user/holdcc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage decentralized agent identities, link agent DIDs to human owners, sign identity challenges, and verify DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and uses long-lived identity credentials.

Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and treat $HOME/.openclaw/billions as a sensitive credential store.

Risk: Imported private keys can be exposed through command-line arguments.

Mitigation: Avoid importing real private keys via command-line arguments.

Risk: Referenced install scripts and package lockfile were not available for review in the submitted artifact.

Mitigation: Verify the missing scripts and package lockfile from a trusted source before running npm install.

## Reference(s):

- [Billions Network](https://billions.network/)
- [ClawHub skill page](https://clawhub.ai/holdcc/skills/verified-agent-identity-3)
- [Publisher profile](https://clawhub.ai/user/holdcc)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce DID strings, challenge strings, JSON identity records, verification status text, and local credential files under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
