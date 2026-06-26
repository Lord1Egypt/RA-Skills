## Description: <br>
Read and manage a signed-in Skylight Calendar family hub, including calendar events, chores and reward stars, shared lists, and frame/device information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent interact with their own Skylight family account for calendar, chore, rewards, list, and frame-management tasks. It is intended for accounts where the user is comfortable configuring Skylight email and password credentials for the MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server requires a Skylight email and password and the security verdict flags the release for review. <br>
Mitigation: Install only if comfortable sharing those credentials, prefer a dedicated account when possible, and keep MCP configuration files private. <br>
Risk: The package is invoked through an external npm MCP server and may be installed without a pinned version. <br>
Mitigation: Pin the npm package version before use and review updates before changing the configured version. <br>
Risk: Tool actions can create, update, delete, or approve family-account items. <br>
Mitigation: Require explicit user confirmation before performing write, delete, approval, or other account-changing actions. <br>


## Reference(s): <br>
- [Skylight](https://www.ourskylight.com) <br>
- [skylight-mcp npm package](https://www.npmjs.com/package/skylight-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown responses with JSON MCP configuration snippets and tool-mediated Skylight account actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Skylight email and password credentials; tool actions are scoped to a Skylight frame and may read or modify family calendar, chores, rewards, shared lists, and frame information.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
