## Description:

Set up Qubrics for agents, register a durable inbox without an existing key, link an owner, choose a runtime surface, and make the first harmless call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure Qubrics for an agent, choose the correct API surface and credential, and verify a connection before making a first harmless call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Management examples may use an existing root credential for queries beyond the skill's stated onboarding purpose.

Mitigation: Review each management operation, verify the selected profile and returned identity, and keep credentials in an approved secret store.

Risk: The skill references an unpinned installation source.

Mitigation: Check the package and release against a trusted source before installing, and pin a verified version when the tool supports it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline shell and TypeScript examples and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Surface-specific setup steps and first-call examples.]

## Skill Version(s):

2.0.8 (source: frontmatter, confirmed by server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
