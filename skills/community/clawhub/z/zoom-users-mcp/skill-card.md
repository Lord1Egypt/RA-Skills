## Description:

MCP server for the Zoom Users API. Exposes Zoom Users' REST API as read-only MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to connect an MCP client to read-only Zoom Users API tools, list available tools, and call those tools through mcporter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client may read Zoom user-directory data.

Mitigation: Install only when that data access is intended and use a scoped credential appropriate for read-only Zoom Users API access.

## Reference(s):

- [npm package](https://www.npmjs.com/package/@mjquinlan2000/zoom-users-mcp)
- [ClawHub skill page](https://clawhub.ai/mjquinlan2000/skills/zoom-users-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter, zoom-users-mcp, and NODE_MCP_SECRET_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
