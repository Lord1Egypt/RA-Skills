## Description: <br>
Use SwarmRecall when an AI agent needs persistent memory, a knowledge graph, learnings, a skill registry, shared pools, or background dream consolidation across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to connect agents to SwarmRecall for persistent memory, knowledge graph operations, learning logs, skill registry lookup, shared pools, and background consolidation through CLI, MCP, HTTP, or SDK workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected agent memory, session context, tool details, logs, and shared-pool data to SwarmRecall's hosted service. <br>
Mitigation: Use the skill only with user consent for external storage, redact personal or regulated data before storage, and avoid storing data that should remain local. <br>
Risk: The skill requires an API key and supports local configuration files that could expose credentials if mishandled. <br>
Mitigation: Use environment-based secret handling or the documented local config, avoid committing API keys, rotate revoked keys, and pass credentials through MCP client environment settings. <br>
Risk: Shared pool writes may expose memory, knowledge, learnings, or skills to other agents with pool access. <br>
Mitigation: Confirm pool membership and access level before writing, and use pool identifiers intentionally for shared data. <br>
Risk: Automatic consolidation and dream workflows can prune, deduplicate, or summarize stored memories. <br>
Mitigation: Understand deletion and retention behavior before enabling automatic consolidation, and prefer dry runs or review loops where available. <br>


## Reference(s): <br>
- [SwarmRecall MCP documentation](https://www.swarmrecall.ai/docs/mcp) <br>
- [CLI command reference](references/commands.md) <br>
- [MCP tools reference](references/mcp-tools.md) <br>
- [Troubleshooting](TROUBLESHOOTING.md) <br>
- [Quickstart example](examples/quickstart.md) <br>
- [SwarmRecall API reference](https://www.swarmrecall.ai/docs/api-reference) <br>
- [SwarmRecall CLI package](https://www.npmjs.com/package/@swarmrecall/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool names, resource URIs, API endpoint references, and operational guidance for storing or retrieving external agent memory.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
