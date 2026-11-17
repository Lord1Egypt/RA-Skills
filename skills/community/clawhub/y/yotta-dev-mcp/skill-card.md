## Description:

A local stdio MCP server that gives coding agents deterministic tools for mapping, reviewing, and verifying software changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the MCP server from compatible coding agents to explore unfamiliar repositories, assess architecture and change impact, review code, and produce evidence-based verification results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A workflow-reading flaw can expose private files outside the selected project to the assistant.

Mitigation: Use trusted projects or the core tool profile until workflow reads reject links and enforce project containment; keep workflow data within reviewed projects.

Risk: Explicitly enabled checks and adapters can execute project code.

Mitigation: Enable checks or adapters only for trusted code, review their configured scope, and opt in only when needed.

Risk: Configuration diagnostics can reveal which local applications have MCP servers configured.

Mitigation: Run diagnostics only in an environment where that inventory is appropriate to disclose.

## Reference(s):

- [Project homepage](https://github.com/YottaMeta/yotta-dev-mcp)
- [ClawHub release page](https://clawhub.ai/yottameta/skills/yotta-dev-mcp)
- [Tool reference](references/tools.md)
- [Architecture contract reference](references/architecture-contract.md)
- [Adapter reference](references/adapters.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text, Guidance]

**Output Format:** [Structured JSON and concise text with file and line evidence where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic, bounded results; command execution and file writes require explicit opt-in.]

## Skill Version(s):

0.2.8 (source: SKILL.md frontmatter, package.json, server.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
