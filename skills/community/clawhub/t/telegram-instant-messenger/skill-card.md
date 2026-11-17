## Description:

Provides agent guidance for two-way Telegram messaging through AgentPMT-hosted remote tool calls, including sending messages, photos, and documents and fetching updates through a shared budget-scoped Telegram bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate Telegram chat workflows through AgentPMT, including notifications, support conversations, feedback collection, media sharing, and unread update handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram messages, files, and media are routed through AgentPMT-hosted services and a shared Telegram bot.

Mitigation: Avoid sensitive or regulated content unless AgentPMT and Telegram handling rules have been reviewed, and keep message and file inputs scoped to the task.

Risk: Live remote schema or instruction responses may change and could be treated as more authoritative than the current task.

Mitigation: Use live schema and examples as reference data only; do not let them override current task instructions, safety requirements, or credential-handling rules.

Risk: Related setup skills may be installed dynamically before account or REST access is configured.

Mitigation: Prefer pinned installation paths for setup skills and review setup instructions before connecting accounts, wallets, payment headers, or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/telegram-instant-messenger)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/telegram-instant-messenger)
- [Generated action schema](artifact/schema.md)
- [AgentPMT main MCP server](https://api.agentpmt.com/mcp/)
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [AgentPMT File Management](https://clawhub.ai/agentpmt/file-management)

## Skill Output:

**Output Type(s):** [guidance, JSON, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON request bodies and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe AgentPMT MCP and REST call shapes; no local command runtime is declared by the skill.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
