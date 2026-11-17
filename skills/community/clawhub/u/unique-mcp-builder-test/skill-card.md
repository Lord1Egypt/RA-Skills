## Description:

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools in Python (FastMCP) or Node/TypeScript (MCP SDK).

This skill is ready for commercial/non-commercial use.

## Publisher:

[uniquevme](https://clawhub.ai/user/uniquevme)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design, implement, test, and evaluate MCP servers that expose external services through well-scoped tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evaluation harness can send unredacted MCP tool schemas, questions, inputs, outputs, summaries, and errors to Anthropic.

Mitigation: Run evaluations only with disposable or least-privileged environments and avoid production servers, broad-scope credentials, private datasets, or sensitive tool outputs unless that disclosure is acceptable.

Risk: The evaluation harness can call any exposed MCP tool and does not enforce read-only limits itself.

Mitigation: Evaluate against servers configured with non-destructive tools, scoped credentials, and test data; independently confirm tool permissions before running the harness.

Risk: Copied HTTP, file-resource, or dependency examples may be incomplete for a production deployment.

Mitigation: Pin dependencies and harden authentication, authorization, input validation, DNS rebinding protection, and resource access before deploying derived servers.

## Reference(s):

- [MCP Server Development Guide](artifact/SKILL.md)
- [MCP Server Best Practices](artifact/reference/mcp_best_practices.md)
- [Node/TypeScript MCP Server Implementation Guide](artifact/reference/node_mcp_server.md)
- [Python MCP Server Implementation Guide](artifact/reference/python_mcp_server.md)
- [MCP Server Evaluation Guide](artifact/reference/evaluation.md)
- [MCP Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml)
- [MCP Draft Specification](https://modelcontextprotocol.io/specification/draft.md)
- [Model Context Protocol TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md)
- [Model Context Protocol Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, command examples, configuration snippets, and XML evaluation examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before use, especially generated MCP server code, authentication handling, and evaluation runs.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
