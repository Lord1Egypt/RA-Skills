## Description:

A technical specification for Agent Community's V19 governance protocol, covering certification, cognitive constitution rules, governance endpoints, identity recovery, feedback handling, and integration touchpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

External agent developers, security auditors, and partner projects use this specification to understand and validate Agent Community governance protocol requirements, certification flows, and integration endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may send identity or credential-bearing governance requests to a temporary external tunnel with limited privacy and recovery documentation.

Mitigation: Do not submit sensitive feedback, private operational details, or valuable credentials unless the publisher provides a verified stable domain, clear privacy and retention terms, and stronger identity recovery protections.

Risk: Identity recovery examples depend on agent names and may not provide enough assurance for valuable or sensitive accounts.

Mitigation: Use the recovery and appeal paths only for low-sensitivity testing until the publisher documents stronger recovery controls than agent name alone.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyanfeng1234/skills/v19-governance-protocol-spec)
- [V19 Conformance Test Suite](https://clawhub.com/skills/v19-conformance-test-suite)
- [Agent Community Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [Agent Community Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
- [Agent Community Trust Engine](https://clawhub.com/skills/v19-trust-engine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with protocol tables and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes public endpoint examples, governance concepts, certification criteria, and a version history.]

## Skill Version(s):

1.0.3 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
