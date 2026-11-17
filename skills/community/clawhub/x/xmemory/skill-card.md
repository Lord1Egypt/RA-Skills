## Description:

Persistent structured memory - save, recall, and update facts, decisions, people, and projects across sessions via the xmemory MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmemory](https://clawhub.ai/user/xmemory)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use xmemory to persist durable facts, preferences, decisions, people, and project state across sessions, then recall or update that saved memory through the xmemory MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects agents to an external memory service that can retain facts across sessions.

Mitigation: Require user confirmation before saving memory, avoid storing secrets or highly sensitive personal data, and use separate least-privilege credentials for normal and admin access.

Risk: The skill encourages proactive persistence of durable facts, which may save information the user did not explicitly ask to store.

Mitigation: Set an agent rule to ask before saving anything and restrict writes to facts the user clearly wants preserved.

Risk: Optional admin and schema-management tools can perform destructive or structural changes, including deleting instances or applying migrations.

Mitigation: Register admin access deliberately, separate it from normal memory access, and require explicit confirmation before destructive or schema-changing operations.

## Reference(s):

- [xmemory homepage](https://xmemory.ai)
- [xmemory console](https://console.xmemory.ai)
- [xmemory ClawHub skill listing](https://clawhub.ai/xmemory/skills/xmemory)
- [xmemory publisher profile](https://clawhub.ai/user/xmemory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agent use of xmemory MCP tools for reading, writing, diagnostics, and schema administration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
