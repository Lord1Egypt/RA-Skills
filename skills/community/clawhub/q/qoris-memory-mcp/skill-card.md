## Description:

Persistent memory for OpenClaw agents via the Qoris MCP server, with explicit save and recall tools for cross-session context and no automatic data capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoris-ai](https://clawhub.ai/user/qoris-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and teams use this skill to give OpenClaw agents explicit, workspace-scoped persistent memory across sessions, projects, and shared team contexts. The skill supports saving, retrieving, searching, updating, and deleting user-selected memories through the Qoris MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores selected agent memories in an external Qoris workspace.

Mitigation: Install only when external persistent memory is intended, and review Qoris retention and deletion controls before using it for confidential work.

Risk: QORIS_API_KEY grants access to the configured workspace memory.

Mitigation: Treat QORIS_API_KEY as a secret, avoid committing it to source control, and rotate it from the Qoris dashboard if exposure is suspected.

Risk: Shared workspaces can expose saved memories to other holders of the same workspace credentials.

Mitigation: Use a separate Qoris workspace for shared, client-specific, sensitive, or enterprise projects.

Risk: Persisted memories may include credentials, regulated data, or other sensitive content if an agent or user explicitly saves them.

Mitigation: Avoid saving credentials or regulated data unless policy allows it and the workspace controls are appropriate.

## Reference(s):

- [Qoris Memory Documentation](https://docs.qoris.ai/memory)
- [Qoris AI Homepage](https://qoris.ai)
- [Qoris Dashboard](https://qoris.ai/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/qoris-ai/skills/qoris-memory-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets; memory and search results are returned as text records from the MCP service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QORIS_API_KEY and QORIS_WORKSPACE_ID environment variables; data is persisted only through explicit memory tool calls.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
