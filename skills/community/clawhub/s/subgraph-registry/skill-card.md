## Description: <br>
Discover and filter 15,500+ The Graph subgraphs by domain, network, protocol type, or natural language goal, with x402 query URLs for $0.01 USDC on Base per call and no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulieb14](https://clawhub.ai/user/paulieb14) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to discover reliable subgraphs on The Graph Network, inspect schemas and classifications, and obtain x402 or legacy query instructions before querying data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags the artifact as suspicious because it bundles an analytics web app with LLM-to-SQL, cloud credential use, and wallet identity enrichment outside the stated MCP purpose. <br>
Mitigation: Install only when the MCP registry is needed, review the bundled dashboard code before deployment, and do not configure Anthropic, AWS, or Graph credentials unless intentionally running that dashboard. <br>
Risk: Returned x402 URLs can trigger USDC spending when followed by an x402-capable client. <br>
Mitigation: Require explicit user approval, wallet separation, and spending limits before an agent signs or retries paid x402 queries. <br>
Risk: The optional HTTP/SSE transport starts a local server on a configurable port. <br>
Mitigation: Prefer the default stdio transport for agent runtimes and bind HTTP transport only in trusted local or isolated environments. <br>
Risk: The registry database is downloaded and cached on first run. <br>
Mitigation: Keep package versions pinned and leave database hash verification enabled unless deliberately rebuilding the registry in a controlled development environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulieb14/skills/subgraph-registry) <br>
- [Project homepage from ClawDIS metadata](https://github.com/PaulieB14/subgraph-registry) <br>
- [MCP server manifest](server.json) <br>
- [OpenAPI 3.1 specification](data/openapi.json) <br>
- [The Graph Network](https://thegraph.com) <br>
- [The Graph Studio API keys](https://thegraph.com/studio/apikeys/) <br>
- [@graphprotocol/client-x402](https://www.npmjs.com/package/@graphprotocol/client-x402) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, code, guidance] <br>
**Output Format:** [MCP tool results with subgraph metadata, query URLs, pricing details, and GraphQL starter-query guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include x402 payment manifests and legacy API-key query URLs; agents should require approval before spending USDC.] <br>

## Skill Version(s): <br>
0.8.7 (source: evidence.release.version, package.json, server.json, and OpenAPI) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
