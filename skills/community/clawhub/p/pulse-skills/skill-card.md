## Description:

Pulse Skills helps agents share and maintain Aicoo/Pulse workspace context through API-guided syncing, note operations, snapshots, share links, agent-to-agent messaging, daily briefings, and inbox monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect AI agents with Aicoo/Pulse workspaces, sync and manage knowledge, create scoped share links, monitor inbox activity, and coordinate agent-to-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated workspace access can expose Aicoo/Pulse notes, files, messages, and sharing state.

Mitigation: Install only when the agent should have authenticated workspace access, keep PULSE_API_KEY private, and review intended API actions before execution.

Risk: Hooks, loops, routines, and cron jobs can sync project or conversation data without enough scoping or confirmation.

Mitigation: Limit automation to explicit Pulse tasks and review which files or messages will be sent before enabling scheduled or event-driven sync.

Risk: All-workspace share scopes can expose more context than intended.

Mitigation: Prefer folder-scoped, read-only, expiring links; audit active links and revoke or narrow broad links when they are not deliberate.

Risk: MCP and integration changes may affect connected external tools.

Mitigation: Treat MCP and OAuth integration changes as admin-level actions and require deliberate review before authorizing, refreshing, disconnecting, or removing integrations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xisen-w/skills/pulse-skills)
- [Aicoo API Documentation](https://www.aicoo.io/docs/api)
- [Aicoo API Keys](https://www.aicoo.io/settings/api-keys)
- [Context Sync API Reference](skills/context-sync/reference/API.md)
- [Share Agent API Reference](skills/share-agent/reference/API.md)
- [Examine Sandbox API Reference](skills/examine-sandbox/reference/API.md)
- [Verified MCP Integrations](assets/integrations/verified-mcps.md)
- [Notion MCP Guide](https://developers.notion.com/guides/mcp/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated Aicoo/Pulse API calls that require PULSE_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
