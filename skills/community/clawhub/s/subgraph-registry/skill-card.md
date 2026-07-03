## Description: <br>
Discover and filter 15,500+ The Graph subgraphs by domain, network, protocol type, or natural language goal; each result includes an x402 query URL for $0.01 USDC on Base per call, no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulieb14](https://clawhub.ai/user/paulieb14) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to discover, compare, and select The Graph subgraphs by domain, network, protocol type, entity, keyword, or natural-language goal before querying them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The x402 workflow can trigger paid USDC queries when connected to an agent wallet. <br>
Mitigation: Require per-call limits or explicit confirmation before enabling automatic wallet spending. <br>
Risk: HTTP/SSE mode can expose a local server when explicitly started. <br>
Mitigation: Run HTTP mode only behind local or trusted access controls in autonomous or shared environments. <br>
Risk: The registry database is downloaded on first run and must match the package-pinned hash. <br>
Mitigation: Keep hash verification enabled and avoid SUBGRAPH_REGISTRY_SKIP_VERIFY unless intentionally rebuilding the registry. <br>
Risk: Dependency hygiene matters for autonomous runtimes. <br>
Mitigation: Pin dependencies and update the MCP SDK before deployment in high-trust environments. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/PaulieB14/subgraph-registry) <br>
- [ClawHub skill page](https://clawhub.ai/paulieb14/skills/subgraph-registry) <br>
- [The Graph Network](https://thegraph.com) <br>
- [OpenAPI specification](data/openapi.json) <br>
- [Graph x402 client package](https://www.npmjs.com/package/@graphprotocol/client-x402) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Configuration] <br>
**Output Format:** [MCP tool responses with structured JSON, query URLs, pricing manifests, and concise query guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include x402 payment URLs and pricing metadata; HTTP/SSE transport is only used when explicitly started.] <br>

## Skill Version(s): <br>
0.8.10 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
