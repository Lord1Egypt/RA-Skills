## Description: <br>
Guides users through configuring a WeCom MCP integration in OpenClaw, including MCP server setup, tool allowlisting, gateway restart, and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stliuexp](https://clawhub.ai/user/stliuexp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill when adding or troubleshooting a WeCom MCP server so agents can access approved WeCom messaging, todo, meeting, schedule, and contact tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup runs a third-party npm package through npx for the MCP server. <br>
Mitigation: Verify the wecom-mcp-server package and publisher before use, and pin a trusted package version where operationally practical. <br>
Risk: The configuration uses WeCom credentials, including WECOM_SECRET. <br>
Mitigation: Keep secrets out of version control, store them only in local configuration, rotate them periodically, and scope credentials to the minimum permissions needed. <br>
Risk: Allowlisting the MCP server gives OpenClaw access to WeCom capabilities exposed by that server. <br>
Mitigation: Enable only the required WeCom tools and review the configured tool permissions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stliuexp/wecom-mcp-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup and troubleshooting instructions; it does not execute commands directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
