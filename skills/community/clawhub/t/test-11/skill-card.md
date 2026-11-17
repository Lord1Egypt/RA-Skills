## Description:

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarrett817](https://clawhub.ai/user/jarrett817)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers for external service integrations in TypeScript or Python.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation runs can expose MCP tool outputs to Anthropic when connected to sensitive or production-backed servers.

Mitigation: Run evaluations only in controlled development environments, avoid production-connected MCP servers unless approved, and sanitize or minimize data returned by tools.

Risk: Generated or example HTTP MCP servers may expose unauthenticated tool endpoints if deployed without additional safeguards.

Mitigation: Require authentication, bind locally or use TLS-safe deployment, enforce origin and host checks, add rate limits, and use least-privilege upstream credentials.

## Reference(s):

- [MCP Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml)
- [MCP Specification Draft](https://modelcontextprotocol.io/specification/draft.md)
- [MCP TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md)
- [MCP Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)
- [MCP Best Practices](reference/mcp_best_practices.md)
- [Node/TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md)
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md)
- [MCP Server Evaluation Guide](reference/evaluation.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and XML evaluation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional Python scripts for connecting to MCP servers and running evaluation tasks.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
