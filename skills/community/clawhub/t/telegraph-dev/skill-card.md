## Description:

Use Telegraph Protocol for verified AI inference across weather and climate data, media authenticity checks, LLM completions, image generation, embeddings, AI text detection, and autonomous signal monitoring, with paid calls routed through x402 USDC micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xwick](https://clawhub.ai/user/0xwick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to route inference tasks through the Telegraph MCP server for verified answers, generated media, embeddings, content moderation, and signal monitoring. It is intended for workflows that can use a USDC-funded burner wallet and external Telegraph network services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid external inference can spend wallet funds and send prompts or media URLs to third-party services.

Mitigation: Use a dedicated burner wallet with minimal funds and avoid sending sensitive prompts or private media URLs.

Risk: The MCP server package and dynamically discovered tools may change over time.

Mitigation: Prefer pinned and audited MCP package versions, and review live tool schemas before use.

Risk: The documented node, engine, and daemon endpoints use plaintext HTTP.

Mitigation: Do not use plaintext endpoints for sensitive work unless the provider supplies authenticated HTTPS or equivalent protections.

## Reference(s):

- [Telegraph Protocol Documentation](https://docs.telegraphprotocol.com)
- [Telegraph MCP Repository](https://github.com/telegraphprotocol/telegraph-mcp)
- [Telegraph MCP README](https://github.com/telegraphprotocol/telegraph-mcp#readme)
- [ClawHub Skill Page](https://clawhub.ai/0xwick/skills/telegraph-dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, JSON configuration snippets, and MCP tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external inference results, paid-call guidance, and local MCP server configuration details.]

## Skill Version(s):

1.1.0 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
