## Description:

Audits information-flow coherence across system modules and returns a weighted collaboration index from 0 to 1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to query a V19 governance service for system coherence scores, health signals, bottleneck indicators, and registration support for monitored agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to contact an undocumented temporary external service with governance keys and agent names.

Mitigation: Use non-sensitive test keys and non-identifying agent names unless the service operator documents ownership, privacy handling, and retention practices.

Risk: Returned coherence scores and bottleneck findings are not independently verified by the release evidence.

Mitigation: Treat service responses as advisory and validate important governance decisions against local telemetry or an independently reviewed monitoring source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/skills/v19-coherence-auditor)
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint usage examples and expected response fields for coherence, health, and registration workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
