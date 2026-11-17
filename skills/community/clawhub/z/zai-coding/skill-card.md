## Description:

Configure OpenClaw to use Z.AI GLM Coding Plan models, region-specific endpoints, model settings, and optional Z.AI MCP tools for coding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelmaz](https://clawhub.ai/user/nelmaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw for Z.AI GLM Coding Plan models, select international or China endpoints, tune coding-oriented settings, and add Z.AI MCP tools for web and repository research.

### Deployment Geography for Use:

Global, with separate international and China region configuration paths.

## Known Risks and Mitigations:

Risk: The skill asks users to configure persistent agent settings, remote MCP tools, and API credentials.

Mitigation: Prefer interactive onboarding or protected secret mechanisms, avoid placing live bearer tokens in shell history, and protect ~/.openclaw/openclaw.json.

Risk: Z.AI MCP tools can send prompts, URLs, repository references, and fetched content to an external provider.

Mitigation: Do not use these tools with confidential URLs, private repositories, secrets, regulated data, or unapproved provider regions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nelmaz/skills/zai-coding)
- [Publisher Profile](https://clawhub.ai/user/nelmaz)
- [Z.AI Coding Plan](https://z.ai/subscribe)
- [BigModel China API Portal](https://bigmodel.cn)
- [OpenClaw Z.AI Provider](https://docs.openclaw.ai/providers/zai)
- [OpenClaw GLM Models Overview](https://docs.openclaw.ai/providers/glm)
- [Web Search MCP](https://docs.z.ai/devpack/mcp/search-mcp-server)
- [Web Reader MCP](https://docs.z.ai/devpack/mcp/reader-mcp-server)
- [Zread MCP](https://docs.z.ai/devpack/mcp/zread-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw configuration commands, JSON snippets, model-selection guidance, and MCP setup steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
