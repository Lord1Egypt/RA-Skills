## Description:

V19 Agent Rating provides differentiated trust-score criteria for cognitive-operations, action-execution, and bridge-scheduling agents, with separate weighting for each agent type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to compare agent trust criteria across cognitive-operations, action-execution, and bridge-scheduling agent types. It provides scoring weights, example validation data, and curl examples for querying a third-party governance service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to call an opaque external tunnel with governance keys and agent identifiers.

Mitigation: Review the service before use, avoid sending sensitive agent metadata, and use only scoped per-user keys.

Risk: Returned ratings may be mistaken for authoritative trust decisions.

Mitigation: Treat ratings as one input and independently validate them before relying on them for real agent trust decisions.

## Reference(s):

- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes agent-type scoring weights and example API requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
