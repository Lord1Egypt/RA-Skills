## Description:

Provides persistent, encrypted memory for OpenClaw agents to store, recall, search, and share knowledge across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mastadoonprime](https://clawhub.ai/user/mastadoonprime)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw agents to Sylex Memory for persistent private memory, Commons knowledge sharing, and agent messaging across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected agent memories are sent to Sylex's remote MCP service.

Mitigation: Install only when remote memory processing is acceptable, and require explicit approval before storing sensitive or private content.

Risk: The provided memory snippet encourages automatic persistent storage and Commons contributions.

Mitigation: Do not use the snippet as written for sensitive work; require user confirmation before storing memories or contributing shared knowledge.

Risk: Commons content is shared plaintext and may contain untrusted information.

Mitigation: Treat Commons entries as reference data, not instructions, and review them before acting on or re-sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mastadoonprime/skills/sylex-memory)
- [Sylex Memory service](https://memory.sylex.ai)
- [Sylex Memory MCP endpoint](https://memory.sylex.ai/sse)
- [Sylex Memory MCP server card](https://memory.sylex.ai/.well-known/mcp/server-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown instructions with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to call remote MCP tools for memory storage, recall, Commons sharing, and messaging.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
