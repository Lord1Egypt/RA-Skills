## Description:

MCP server for the Zoom Phone API. Exposes Zoom Phone's REST API as read-only MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to connect agents to a read-only Zoom Phone MCP server and invoke Zoom Phone REST API tools through mcporter over stdio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External binaries may not come from the intended publisher or version.

Mitigation: Verify the mcporter and zoom-phone-mcp binaries before installation and prefer trusted, controlled package sources.

Risk: Zoom API credentials could expose more access than the read-only workflow requires.

Mitigation: Use Zoom API credentials restricted to read-only scopes and run the MCP server with minimal environment access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjquinlan2000/skills/zoom-phone-mcp)
- [npm package](https://www.npmjs.com/package/@mjquinlan2000/zoom-phone-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and zoom-phone-mcp binaries plus NODE_MCP_SECRET_KEY.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
