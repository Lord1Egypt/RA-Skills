## Description: <br>
Set up and authenticate the Xpoz MCP server for social media intelligence. Required by all Xpoz skills. Handles server configuration, OAuth login, and connection verification with minimal user interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure the Xpoz MCP server, complete OAuth authentication, and verify access before running Xpoz social media intelligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the remote/headless OAuth helper can run unintended local code if it receives a crafted authorization code. <br>
Mitigation: Prefer the normal browser login flow; avoid the remote/headless authorization-code helper until it is fixed to pass the code safely as data and clean temporary OAuth state on all failure paths. <br>
Risk: Using this setup connects an Xpoz account to OpenClaw for social media search. <br>
Mitigation: Install only when that account connection is intended, and confirm the OAuth authorization in the browser before completing setup. <br>


## Reference(s): <br>
- [Xpoz Website](https://xpoz.ai) <br>
- [Xpoz MCP Server](https://mcp.xpoz.ai/mcp) <br>
- [Xpoz OAuth Authorization Server Metadata](https://mcp.xpoz.ai/.well-known/oauth-authorization-server) <br>
- [Xpoz Setup on ClawHub](https://clawhub.ai/atyachin/xpoz-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, network access to mcp.xpoz.ai and www.xpoz.ai, and an Xpoz account authenticated with Google OAuth.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
