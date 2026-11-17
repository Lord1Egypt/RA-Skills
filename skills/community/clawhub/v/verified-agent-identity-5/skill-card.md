## Description:

Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agungprabowo123](https://clawhub.ai/user/agungprabowo123)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to create and manage Billions/Iden3 decentralized identities, link an agent identity to a human owner, and sign or verify ownership challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or import identity private keys and store them unencrypted under the user's home directory.

Mitigation: Use a fresh, low-risk identity key and restrict permissions on $HOME/.openclaw/billions before using the skill.

Risk: Signed tokens and verification links produced by the skill can act as sensitive authentication material.

Mitigation: Share signed tokens and verification links only with the intended recipient and avoid exposing them in logs or public channels.

Risk: Installing through an @latest flow can change the code fetched in sensitive environments.

Mitigation: Pin and review the intended skill version before installation when identity material or authentication flows are involved.

## Reference(s):

- [Billions Network](https://billions.network/)
- [ClawHub skill page](https://clawhub.ai/agungprabowo123/skills/verified-agent-identity-5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update identity data under $HOME/.openclaw/billions when its scripts are run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
