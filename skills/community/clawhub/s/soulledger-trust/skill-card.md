## Description:

Query AI agent trust scores, behavioral DNA, and identity verification via SoulLedger protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check an AI agent's trust score, behavioral profile, directory registration, and hash-chain identity signals before interaction or integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts external SoulLedger services to query trust data, behavioral profiles, registration records, and chain verification.

Mitigation: Use the read-only trust, DNA, and directory queries when external network use is acceptable for the environment.

Risk: Agent registration can create an external identity and return an API key.

Mitigation: Confirm registration intent before use and handle any returned API key as a secret.

Risk: The optional npm SDK adds third-party package dependency risk in sensitive environments.

Mitigation: Pin and review @sputnikx/soulledger-sdk before installing it in production or sensitive systems.

## Reference(s):

- [SoulLedger homepage](https://soulledger.sputnikx.xyz)
- [SoulLedger API base URL](https://soul.sputnikx.xyz)
- [ClawHub skill page](https://clawhub.ai/drivenbymyai-max/skills/soulledger-trust)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce curl requests, SDK installation commands, and concise guidance for trust, DNA, directory, registration, and chain verification workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
