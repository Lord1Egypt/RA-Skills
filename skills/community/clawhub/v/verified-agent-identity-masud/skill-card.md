## Description:

Verified Agent Identity Masud helps agents create, manage, link, prove, and verify Billions Network decentralized identities using iden3-based cryptographic signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masudijkp003-star](https://clawhub.ai/user/masudijkp003-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to create Billions Network DIDs, link an agent DID to a human owner, and run challenge signing or signature verification flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-lived agent identity keys under $HOME/.openclaw/billions.

Mitigation: Install only in environments where this storage location is acceptable and configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities.

Risk: Real private keys passed on the command line may be exposed through shell history or process inspection.

Mitigation: Avoid passing real private keys on the command line.

Risk: Generated proofs and linking URLs can be sensitive.

Mitigation: Treat generated proofs and linking URLs as sensitive material and share them only with intended parties.

Risk: The security evidence recommends review before production trust decisions.

Mitigation: Review the dependency state and authentication challenge behavior before using the skill for production trust decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/masudijkp003-star/skills/verified-agent-identity-masud)
- [Billions Network](https://billions.network/)
- [Skill usage instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or string script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce DIDs, verification URLs, signed challenge status, identity listings, and local configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
