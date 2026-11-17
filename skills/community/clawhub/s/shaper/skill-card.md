## Description:

Connect to a Shaper workspace via MCP so an agent can orient on active Shape Up work, read pitch context, create or track scopes, update hill chart progress, and complete scopes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jax-agent](https://clawhub.ai/user/jax-agent)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and project teams use this skill to let an agent work inside a Shaper workspace: read active cycle and pitch context, manage scopes, update hill chart progress, and mark work complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Shaper API key and does not fully explain credential handling.

Mitigation: Use a revocable, least-privilege API key for a workspace the user is comfortable letting an agent access, and avoid pasting secrets into chat.

Risk: The available tool reference includes an unauthenticated workspace-registration flow that can create a workspace and return new credentials.

Mitigation: Require explicit user confirmation before workspace registration or any action that creates or returns credentials.

Risk: The skill can create pitches and scopes, update hill chart progress, and complete scopes in a live workspace.

Mitigation: Confirm with the user before pitch creation, scope creation, scope updates, or completion actions.

## Reference(s):

- [Shaper MCP Tool Reference](references/tools.md)
- [Shaper MCP Discovery](https://useshaper.com/.well-known/mcp.json)
- [Shaper Skill Page](https://clawhub.ai/jax-agent/skills/shaper)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Shaper workspace slug and API key for authenticated workspace operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
