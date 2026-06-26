## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarrett817](https://clawhub.ai/user/jarrett817) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers for external APIs or services in TypeScript or Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled evaluator can allow Claude to call tools on a connected MCP server and send tool results to Anthropic without enforcing read-only limits. <br>
Mitigation: Run evaluations only against test or read-only MCP servers, avoid real accounts or write-capable tools, and assume tool outputs may be sent to Anthropic during evaluation. <br>


## Reference(s): <br>
- [MCP Best Practices](reference/mcp_best_practices.md) <br>
- [TypeScript MCP Server Guide](reference/node_mcp_server.md) <br>
- [Python MCP Server Guide](reference/python_mcp_server.md) <br>
- [MCP Server Evaluation Guide](reference/evaluation.md) <br>
- [Model Context Protocol sitemap](https://modelcontextprotocol.io/sitemap.xml) <br>
- [Model Context Protocol draft specification](https://modelcontextprotocol.io/specification/draft.md) <br>
- [TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md) <br>
- [Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks, command examples, and XML evaluation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of MCP server source files and evaluation artifacts; review commands and generated files before use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
