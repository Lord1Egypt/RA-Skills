## Description:

Write reusable WGSL filters, transitions, and generators for Levea's ShaderFX ABI v2 and v3, previewing effects in WebGPU and exporting them through Vulkan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT

## Use Case:

Video editors and developers use this skill to write and apply reusable WGSL GPU filters, transitions, and generators in Levea projects, then preview and export the resulting effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the documented Levea service requires an account and API key for the self-hosted MCP setup.

Mitigation: Keep the API key in the MCP server or plugin's secret configuration, and confirm the service connection is appropriate before use.

Risk: The security review was partial and could not resolve several local path-like references.

Mitigation: Review the referenced local files and setup details before installing or running the skill.

## Reference(s):

- [ShaderFX Effects on ClawHub](https://clawhub.ai/brajendrak00068/skills/shaderfx-effects)
- [Levea API](https://api.livecore.ai)
- [Levea Hosted MCP](https://api.livecore.ai/api/v1/misc/mcp)

## Skill Output:

**Output Type(s):** [Code, Configuration, API Calls, Guidance]

**Output Format:** [WGSL source, JSON manifests, and structured tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe reusable filters, transitions, generators, and their parameters or resources.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
