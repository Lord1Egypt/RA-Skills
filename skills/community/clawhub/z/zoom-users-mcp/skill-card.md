## Description: <br>
MCP server for the Zoom Users API that exposes Zoom Users' REST API as read-only MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a read-only Zoom Users MCP server, list available tools, and call Zoom user-related tools through mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Zoom API secret could expose user data if mishandled or over-permissioned. <br>
Mitigation: Store NODE_MCP_SECRET_KEY in approved secret management and configure the Zoom credential with the narrowest read-only user scope needed. <br>
Risk: The skill depends on a third-party npm package that is not bundled in the submitted artifact. <br>
Mitigation: Install only if the referenced zoom-users-mcp package is trusted and matches the expected release. <br>


## Reference(s): <br>
- [npm package: @mjquinlan2000/zoom-users-mcp](https://www.npmjs.com/package/@mjquinlan2000/zoom-users-mcp) <br>
- [ClawHub release page](https://clawhub.ai/mjquinlan2000/zoom-users-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, zoom-users-mcp, and NODE_MCP_SECRET_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
