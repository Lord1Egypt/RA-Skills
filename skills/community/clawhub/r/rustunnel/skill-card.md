## Description:

Rustunnel exposes local HTTP/TCP services through secure tunnels and creates public URLs for testing, webhooks, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joaoh82](https://clawhub.ai/user/joaoh82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Rustunnel to expose local HTTP or TCP services for webhook testing, preview sharing, CI/CD preview environments, mobile testing, and controlled tunnel workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose local HTTP/TCP services, including databases or administrative ports, to the public internet.

Mitigation: Use it only for services with strong authentication, least-privilege access, encryption, and a clear need for public reachability.

Risk: Tunnels may remain reachable longer than intended if lifecycle cleanup is missed.

Mitigation: Prefer the MCP create_tunnel and close_tunnel workflow, track tunnel IDs, list active tunnels, and close tunnels promptly after use.

Risk: The source-build installation path includes an unpinned sudo install flow.

Mitigation: Prefer verified or pinned installation methods before installing rustunnel components.

## Reference(s):

- [Rustunnel ClawHub Skill Page](https://clawhub.ai/joaoh82/skills/rustunnel)
- [Rustunnel GitHub Repository](https://github.com/joaoh82/rustunnel)
- [MCP Server Documentation](https://github.com/joaoh82/rustunnel/blob/main/docs/mcp-server.md)
- [API Reference](https://github.com/joaoh82/rustunnel/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, MCP tool calls]

**Output Format:** [Markdown with inline YAML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public tunnel URLs, tunnel IDs, region details, and CLI fallback commands.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
