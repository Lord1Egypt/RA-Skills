## Description: <br>
ToolRouter Gateway provides unified access to ToolRouter tools as OpenClaw tools, including discovery, proxying, caching, usage tracking, and MCP transport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to discover ToolRouter tools, check gateway status, and route approved tool calls through a ToolRouter API key with local caching and usage tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad third-party gateway and can expose high-impact ToolRouter capabilities that are not tightly scoped by the artifact. <br>
Mitigation: Review each requested tool, target, and action before use, and only run scanning, scraping, posting, or account-affecting tools when explicitly authorized. <br>
Risk: Tool calls require a ToolRouter API key and may incur third-party usage costs. <br>
Mitigation: Use a dedicated low-privilege API key with spending controls where available, and monitor usage through the skill status and ToolRouter account controls. <br>
Risk: The skill can persist cached tool responses and usage logs in the workspace memory directory. <br>
Mitigation: Avoid sending secrets or regulated data through the gateway, and disable or clear caching before sensitive work. <br>


## Reference(s): <br>
- [ToolRouter](https://toolrouter.com) <br>
- [ToolRouter MCP endpoint](https://api.toolrouter.com/mcp) <br>
- [ClawHub listing](https://clawhub.ai/neroagent/toolrouter-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON tool responses and Markdown guidance with inline shell and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLROUTER_API_KEY for live ToolRouter access; may write cache and usage logs under the workspace memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
