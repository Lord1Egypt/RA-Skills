## Description:

SwarmRecall helps an AI agent use persistent memory, a knowledge graph, learnings, a skill registry, shared pools, and background dream consolidation across sessions through the SwarmRecall CLI, MCP transports, HTTP, or SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use SwarmRecall to connect agents to persistent memory, semantic knowledge retrieval, learning logs, shared pools, and background consolidation through MCP, CLI, HTTP, or SDK workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent memories, learnings, sessions, and related context are sent to and retained by SwarmRecall servers.

Mitigation: Install only when this remote storage model is acceptable, obtain user consent before storing user-provided content, and review retention and deletion controls before using it for sensitive workflows.

Risk: Raw logs, credentials, regulated data, private project output, or other sensitive content could be stored through memory or learnings workflows.

Mitigation: Avoid storing secrets or confidential data, sanitize logs before using learning workflows, and restrict stored entries to content the user has approved for external retention.

Risk: Authenticated use depends on a SwarmRecall API key and the active API URL.

Mitigation: Prefer environment-based secret handling, keep API keys out of source control, verify the active API URL before use, and rotate or revoke keys when needed.

## Reference(s):

- [SwarmRecall MCP documentation](https://www.swarmrecall.ai/docs/mcp)
- [SwarmRecall API reference](https://www.swarmrecall.ai/docs/api-reference)
- [SwarmRecall CLI package](https://www.npmjs.com/package/@swarmrecall/cli)
- [SwarmRecall remote MCP endpoint](https://swarmrecall-api.onrender.com/mcp)
- [ClawHub skill page](https://clawhub.ai/waydelyle/skills/swarmrecall)
- [Commands reference](artifact/references/commands.md)
- [MCP tools reference](artifact/references/mcp-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP, CLI, SDK, or HTTP operations whose tool responses are stringified JSON.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
