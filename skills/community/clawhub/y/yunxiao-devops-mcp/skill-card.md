## Description:

云效 DevOps MCP helps agents operate Alibaba Cloud Yunxiao through an MCP SSE server for project, work item, pipeline, repository, and deployment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonasgao](https://clawhub.ai/user/jonasgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to discover Yunxiao MCP tools, inspect tool schemas, and call DevOps operations for project tracking, work item management, pipeline runs, repository operations, and deployment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A credential-backed DevOps MCP service can expose broad write powers over unauthenticated HTTP.

Mitigation: Bind the MCP server to 127.0.0.1 or place it behind authenticated TLS, use a dedicated least-privileged RAM identity, and require explicit approval before tools create, update, deploy, or change repository content.

Risk: Plaintext environment secrets can expose Alibaba Cloud RAM credentials.

Mitigation: Protect or avoid plaintext .env secrets, rotate credentials after exposure, and review audit logs if the service was reachable from an untrusted network.

Risk: A mutable container image can change server behavior after review.

Mitigation: Pin the MCP server image to a reviewed digest before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonasgao/skills/yunxiao-devops-mcp)
- [Alibaba Cloud Yunxiao documentation](https://help.aliyun.com/zh/yunxiao/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and guidance, JSON tool schemas and tool results, JavaScript examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a separately deployed Yunxiao MCP SSE server and valid Alibaba Cloud credentials; tool effects depend on the configured Yunxiao permissions.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
