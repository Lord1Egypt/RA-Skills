## Description:

Consult public ratings for known websites or agents and submit honest, signed feedback after a real interaction when authorized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mathieucollaaithos](https://clawhub.ai/user/mathieucollaaithos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can consult public website or agent ratings as reputation evidence and, after a genuine interaction, publish authorized signed feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public rating could disclose private information or misrepresent an interaction and cannot be edited or deleted.

Mitigation: Publish only when authorized after a real interaction; confirm the target, score, and public comment before submission and omit private information.

Risk: Installing an external CLI can execute unreviewed code, and exposure of the signing key can compromise the rating identity.

Mitigation: Review the external checkout and install/build scripts before execution; keep the signing key local and out of logs, version control, and messages.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mathieucollaaithos/skills/rank-anything)
- [Rank Anything API documentation](https://rank.aithos.world/docs/)
- [Rank Anything OpenAPI specification](https://rank.aithos.world/openapi.json)
- [Signing profile](https://github.com/Math1987/agentrate/blob/main/docs/authentication.md)
- [Resource identifiers](https://github.com/Math1987/agentrate/blob/main/docs/resource-identifiers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with optional shell commands and rating summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing requires explicit authorization and confirmation of the accepted rating.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
