## Description: <br>
Expose local services via secure tunnels using the rustunnel MCP server, creating public URLs for local HTTP/TCP services for testing, webhooks, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaoh82](https://clawhub.ai/user/joaoh82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Rustunnel to expose local HTTP or TCP services for webhook testing, demos, preview environments, mobile testing, and temporary access workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating public tunnels can expose local services, including databases or administrative interfaces, to the internet. <br>
Mitigation: Confirm the exact local port and protocol before creating a tunnel, avoid exposing sensitive services unless they are separately secured, and close tunnels promptly when finished. <br>
Risk: The skill reads a rustunnel access token from ~/.rustunnel/config.yml. <br>
Mitigation: Protect the config file with restrictive permissions, avoid printing or sharing the token, and rotate or remove the token when it is no longer needed. <br>
Risk: CLI fallback mode can leave tunnel processes running outside the MCP lifecycle. <br>
Mitigation: Prefer MCP create_tunnel and close_tunnel flows; when using the CLI fallback, stop the process manually and verify active tunnels before considering the workflow complete. <br>


## Reference(s): <br>
- [Rustunnel skill page](https://clawhub.ai/joaoh82/rustunnel) <br>
- [GitHub Repository](https://github.com/joaoh82/rustunnel) <br>
- [MCP Server Documentation](https://github.com/joaoh82/rustunnel/blob/main/docs/mcp-server.md) <br>
- [API Reference](https://github.com/joaoh82/rustunnel/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public tunnel URLs, tunnel IDs, MCP tool parameters, and CLI fallback commands.] <br>

## Skill Version(s): <br>
1.3.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
