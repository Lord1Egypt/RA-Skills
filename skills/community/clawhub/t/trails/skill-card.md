## Description: <br>
Integrate Trails cross-chain infrastructure — Widget, Headless SDK, or Direct API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesLawton](https://clawhub.ai/user/JamesLawton) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to choose and implement the right Trails integration path for cross-chain payments, swaps, token bridging, and destination contract execution. It supports React widget integrations, React headless SDK flows, and direct API usage for backend or non-React systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through payment, swap, bridge, calldata, and batch-settlement flows that move blockchain assets. <br>
Mitigation: Manually review every generated transaction flow, destination address, token, chain, calldata payload, and settlement path before signing or deploying. <br>
Risk: The skill instructs agents to search project files and environment variables for Trails API keys. <br>
Mitigation: Restrict agent access to Trails-specific environment variables and avoid exposing privileged or unrelated API keys in client-side code. <br>
Risk: Unpinned package installation examples may change behavior as upstream packages evolve. <br>
Mitigation: Pin package versions in production projects and validate generated Trails integrations against the current Trails documentation before release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JamesLawton/trails) <br>
- [Trails Documentation](https://docs.trails.build) <br>
- [Trails Docs MCP](https://docs.trails.build/mcp) <br>
- [Trails API Reference](https://docs.trails.build/api) <br>
- [Trails SDK Reference](https://docs.trails.build/sdk) <br>
- [Trails Product Site](https://trails.build) <br>
- [TRAILS_OVERVIEW.md](docs/TRAILS_OVERVIEW.md) <br>
- [INTEGRATION_DECISION_TREE.md](docs/INTEGRATION_DECISION_TREE.md) <br>
- [API_RECIPES.md](docs/API_RECIPES.md) <br>
- [CALLDATA_GUIDE.md](docs/CALLDATA_GUIDE.md) <br>
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline TypeScript, TSX, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Trails API key environment-variable guidance, package installation commands, React component snippets, API request examples, and calldata encoding examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
