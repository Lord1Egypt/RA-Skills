## Description:

Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitrisetiadi](https://clawhub.ai/user/ajitrisetiadi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to create and manage Billions/Iden3 decentralized identities, sign authentication challenges, link an agent DID to a human owner, and verify identity ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or import an agent identity whose private key may be stored unencrypted under $HOME/.openclaw/billions.

Mitigation: Review the skill before installing, restrict access to the storage directory, and proceed only when unencrypted local key storage is acceptable.

Risk: The skill can sign challenges, link a human owner, and send verification messages.

Mitigation: Require explicit user confirmation before creating identities, signing challenges, linking owners, or sending verification messages.

Risk: Replacement scripts or dependencies from an unreviewed source could change identity or signing behavior.

Mitigation: Use reviewed artifact files and dependencies only; do not run substituted scripts or dependency sets without review.

## Reference(s):

- [Billions Network](https://billions.network/)
- [ClawHub Skill Page](https://clawhub.ai/ajitrisetiadi/skills/verified-agent-identity-ajitrisetiadi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and openclaw; identity data is stored under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
