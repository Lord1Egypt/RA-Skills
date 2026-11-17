## Description:

Enables agents to manage decentralized identities, generate pairwise DIDs, sign B2B mandates, and create selective disclosure proofs for privacy-preserving interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tamtunnel](https://clawhub.ai/user/tamtunnel)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent builders use this skill to give agents local DID-based identity workflows, signed mandates for B2B interactions, and selective disclosure proofs for B2C or access scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity keys and signed mandates are high-value security material.

Mitigation: Run the skill only in an isolated environment with a strong CLAW_PASSWORD and avoid sharing generated key material or password values.

Risk: Generated mandates may be mistaken for authoritative authorization.

Mitigation: Independently validate the issuer, key, expiration, and replay protections before relying on a mandate.

Risk: Selective disclosure examples can expose personal claims if populated with real user data.

Mitigation: Avoid using real personal claims with the selective disclosure script unless the disclosure set and verifier behavior have been reviewed.

Risk: Dependency installation and npx execution can introduce supply-chain exposure.

Mitigation: Pin and review dependencies before running npm or npx commands.

## Reference(s):

- [Skill page](https://clawhub.ai/tamtunnel/skills/sovereign-id)
- [Publisher profile](https://clawhub.ai/user/tamtunnel)
- [README.md](artifact/README.md)
- [AGENT.md](artifact/AGENT.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, TypeScript script invocations, JSON identity artifacts, JWS signatures, and SD-JWT presentations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local execution with CLAW_PASSWORD for encrypted identity key handling.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
