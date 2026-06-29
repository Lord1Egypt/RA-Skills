## Description: <br>
Discover and filter 15,500+ The Graph subgraphs by domain, network, protocol type, or natural language goal, returning reliability-scored results with x402 and legacy query URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulieb14](https://clawhub.ai/user/paulieb14) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this MCP server to find suitable The Graph subgraphs, compare reliability signals, retrieve schemas and endpoints, and choose between x402 paid queries or legacy Studio API-key flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An autonomous agent could follow paid x402 query URLs and spend USDC without explicit budget controls. <br>
Mitigation: Require approved budgets, wallet restrictions, and per-query confirmation before agents use x402 URLs. <br>
Risk: Studio API keys or signing wallets could be mishandled in autonomous runtimes. <br>
Mitigation: Keep credentials out of prompts and logs, scope credentials tightly, and allow access only from trusted clients. <br>
Risk: HTTP/SSE mode can expose the local MCP server beyond the intended client. <br>
Mitigation: Run HTTP/SSE mode only on trusted networks and restrict access to localhost or controlled infrastructure. <br>
Risk: Bypassing registry database verification can load untrusted or locally altered data. <br>
Mitigation: Do not set SUBGRAPH_REGISTRY_SKIP_VERIFY=1 unless you intentionally built the database and verified its source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulieb14/skills/subgraph-registry) <br>
- [Publisher profile](https://clawhub.ai/user/paulieb14) <br>
- [Project homepage](https://github.com/PaulieB14/subgraph-registry) <br>
- [OpenAPI specification](artifact/openapi.yaml) <br>
- [The Graph Network](https://thegraph.com) <br>
- [Graph x402 client package](https://www.npmjs.com/package/@graphprotocol/client-x402) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance, API calls] <br>
**Output Format:** [MCP tool responses and REST/OpenAPI JSON with subgraph rankings, details, query URLs, pricing manifests, and query instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include x402 query URLs that require about $0.01 USDC on Base per query, plus legacy query URLs that require a Graph Studio API key.] <br>

## Skill Version(s): <br>
0.8.9 (source: package.json, server.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
