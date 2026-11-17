## Description:

Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferdiannsy33-pixel](https://clawhub.ai/user/ferdiannsy33-pixel)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to create and manage Billions/Iden3 decentralized identities, sign verification challenges, verify DID ownership, and link an agent identity to a human owner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create persistent cryptographic keys and store identity data under $HOME/.openclaw/billions, including unencrypted private keys.

Mitigation: Use the skill only where persistent local identity storage is acceptable, protect the host account, and prefer encrypted or OS-backed key storage before using the identity for important workflows.

Risk: A private key supplied on the command line may be exposed through shell history or process inspection.

Mitigation: Avoid passing private keys as command-line arguments unless the environment and history handling are controlled.

Risk: The server security summary says the release relies on missing or unreviewed scripts.

Mitigation: Verify scripts and dependencies from a trusted source before setup, and stop immediately if any identity script fails.

## Reference(s):

- [Billions Network](https://billions.network/)
- [ClawHub Skill Page](https://clawhub.ai/ferdiannsy33-pixel/skills/verified-agent-identity-2)
- [Publisher Profile](https://clawhub.ai/user/ferdiannsy33-pixel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create or use local identity files under $HOME/.openclaw/billions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
