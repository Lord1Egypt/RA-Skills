## Description: <br>
MCP server for the Zoom Phone API. Exposes Zoom Phone's REST API as read-only MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with a read-only MCP server that exposes Zoom Phone REST API tools through mcporter over stdio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on external mcporter and zoom-phone-mcp binaries plus credentials that can read Zoom Phone data available to the configured account. <br>
Mitigation: Install only trusted binaries, use least-privileged Zoom/API credentials, and avoid broad admin access unless required. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/mjquinlan2000/zoom-phone-mcp) <br>
- [npm package](https://www.npmjs.com/package/@mjquinlan2000/zoom-phone-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, zoom-phone-mcp, and NODE_MCP_SECRET_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
