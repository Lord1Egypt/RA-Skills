## Description:

Tolstoy MCP configures OpenClaw to connect to Tolstoy's MCP server for video commerce workflows including widgets, media, AI video, product catalog access, publishing, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russell-sketch](https://clawhub.ai/user/russell-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and e-commerce operators use this skill to connect OpenClaw to a Tolstoy workspace, then use agent-assisted workflows to create widgets, manage video media, generate AI videos, search products, publish commerce content, and query analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may be able to publish, delete, or manage live commerce and social content in the connected Tolstoy workspace.

Mitigation: Review outputs and requested tool actions before sending content live, especially for store, social, ads, analytics, publish, and delete workflows.

Risk: OAuth authorization can persist across sessions for the selected Tolstoy workspace.

Mitigation: Install only for trusted Tolstoy workspaces and confirm how to revoke the Tolstoy OAuth authorization when access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/russell-sketch/skills/tolstoy-mcp)
- [Tolstoy Platform](https://platform.gotolstoy.com)
- [Tolstoy MCP Integration Settings](https://platform.gotolstoy.com/settings/integrations/mcp)
- [Tolstoy Homepage](https://gotolstoy.com)
- [OpenClaw](https://openclaw.ai)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local OpenClaw configuration file through setup.js when the user runs the provided command.]

## Skill Version(s):

1.0.0 (source: server release metadata, claw.json, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
