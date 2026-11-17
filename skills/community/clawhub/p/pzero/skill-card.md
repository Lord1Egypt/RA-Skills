## Description:

Point OpenClaw at PZERO prepaid inference using OpenAI-compatible chat completions, a Bearer pzero_ key, and a custom provider configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffcryptoo](https://clawhub.ai/user/jeffcryptoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure PZERO as a custom OpenAI-compatible chat completions provider, choose a live PZERO model ID, and smoke test authenticated inference before making it the default model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PZERO API keys and authorized requests could expose account access, billing activity, or request data to PZERO services.

Mitigation: Keep PZERO_API_KEY private and scoped, verify billing and data-handling expectations before use, and send requests only when using PZERO is intended.

Risk: An incorrect or unverified model ID could route OpenClaw defaults to a model that does not support the expected input type.

Mitigation: Fetch the live model list, select an appropriate text or vision-capable model, and smoke test chat completions before setting it as the default.

Risk: The optional hosted MCP endpoint receives authorized requests when configured with the same bearer token.

Mitigation: Enable the MCP endpoint only when needed and apply the same credential privacy and request-data review used for chat completions.

## Reference(s):

- [PZERO Agents](https://pzero.studio/agents)
- [OpenClaw custom providers and base URLs](https://docs.openclaw.ai/gateway/config-tools#custom-providers-and-base-urls)
- [PZERO models endpoint](https://api.pzero.studio/v1/models)
- [PZERO MCP documentation](https://docs.pzero.studio/agents/mcp)
- [PZERO ClawHub release](https://clawhub.ai/jeffcryptoo/skills/pzero)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON configuration and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PZERO_API_KEY and curl; authenticated calls require confirmed prepaid USDC balance.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
