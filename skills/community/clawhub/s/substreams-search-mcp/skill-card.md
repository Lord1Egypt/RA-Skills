## Description: <br>
Search, inspect, and analyze Substreams packages from the substreams.dev registry - module graphs, protobuf types, and sink deployment commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaulieB14](https://clawhub.ai/user/PaulieB14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover Substreams packages, inspect package module graphs and protobuf outputs, and generate sink deployment guidance for supported blockchain data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional HTTP/SSE transport can expose the MCP server if bound on a reachable network. <br>
Mitigation: Prefer stdio for local use and avoid exposing the HTTP/SSE endpoint to untrusted networks. <br>
Risk: Package inspection fetches and parses user-provided .spkg URLs. <br>
Mitigation: Use trusted .spkg URLs when running inspection and sink configuration tools. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/PaulieB14/substreams-search-mcp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/PaulieB14) <br>
- [OpenClaw homepage](https://github.com/PaulieB14/substreams-search-mcp) <br>
- [Substreams registry](https://substreams.dev) <br>
- [npm package](https://www.npmjs.com/package/substreams-search-mcp) <br>
- [Glama MCP listing](https://glama.ai/mcp/servers/@PaulieB14/substreams-search-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text and JSON-like MCP tool responses, with Markdown diagrams and shell command snippets when sink guidance is available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package metadata, module dependency graphs, protobuf type summaries, Mermaid diagrams, SQL schema snippets, endpoint information, and ready-to-run sink commands.] <br>

## Skill Version(s): <br>
1.3.2 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
