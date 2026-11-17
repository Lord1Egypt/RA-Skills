## Description:

Provides CLI and MCP tools for VMware Private AI GPU inventory, utilization, vGPU profiles and assignment, PAIS model visibility, readiness checks, sizing, and local air-gap bundle inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use the skill to inspect VMware GPU and vGPU resources, review PAIS models and knowledge bases, and safely plan or apply a vGPU profile change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious with medium confidence, citing TLS verification bypass guidance and a credential-issuing capability not disclosed in its stated purpose; scan coverage is partial.

Mitigation: Review the suspicious verdict before installation, including whether issuing a token for another user is appropriate. Keep TLS verification enabled when credentials or sensitive traffic are involved, and do not treat the partial scan as proof of safety.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-privateai)
- [Capabilities](references/capabilities.md)
- [Setup Guide](references/setup-guide.md)
- [CLI Reference](references/cli-reference.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Operational guidance]

**Output Format:** [CLI text and structured MCP JSON, with shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on configured VMware and PAIS services; sizing and local bundle inspection can run without connecting to a model provider.]

## Skill Version(s):

2.5.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
