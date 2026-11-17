## Description:

V19 Conformance Test Suite v1.0.0 helps external developers run five zero-configuration checks for health, self-service registration, audit calls, schema consistency, and documentation reachability against the V19 governance protocol baseline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent engineers use this skill to check whether an agent meets V19 governance protocol baseline certification requirements before pursuing higher trust-score or VPAV validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced Python test script is not bundled with the skill, so users cannot verify its behavior from this artifact alone.

Mitigation: Obtain V19_Conformance_Test_Suite.py from a trusted source and review it before execution.

Risk: The described workflow may contact an external service and create credentials.

Mitigation: Confirm the target service, transmitted data, and credential creation or storage behavior before running the script.

Risk: No server-resolved GitHub import provenance is available for this version.

Mitigation: Treat source origin as unavailable and avoid inferring repository provenance from the skill text.

## Reference(s):

- [V19 Governance Protocol Spec](https://clawhub.com/skills/v19-governance-protocol-spec)
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes a Python conformance test workflow and example pass/fail output.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
