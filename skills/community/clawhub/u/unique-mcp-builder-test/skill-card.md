## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uniquevme](https://clawhub.ai/user/uniquevme) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers for external APIs or services in TypeScript or Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation scripts can connect to MCP servers and invoke their tools, including tools that may be write-capable. <br>
Mitigation: Run evaluations only against trusted local or test MCP servers with least-privilege credentials and non-sensitive data. <br>
Risk: Evaluation reports may capture prompts, tool outputs, and feedback from the connected server. <br>
Mitigation: Review saved reports before sharing or storing them, and avoid using sensitive production data during evaluation. <br>
Risk: Generated MCP implementation guidance may still require project-specific security review before deployment. <br>
Mitigation: Review authentication, tool annotations, error handling, and write-capable operations before deploying an MCP server built from this guidance. <br>


## Reference(s): <br>
- [MCP Best Practices](reference/mcp_best_practices.md) <br>
- [Node/TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md) <br>
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md) <br>
- [MCP Server Evaluation Guide](reference/evaluation.md) <br>
- [Model Context Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml) <br>
- [Model Context Protocol Draft Specification](https://modelcontextprotocol.io/specification/draft.md) <br>
- [Model Context Protocol TypeScript SDK](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md) <br>
- [Model Context Protocol Python SDK](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, XML examples, and configuration patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional evaluation scripts that can connect to MCP servers over stdio, SSE, or streamable HTTP.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
