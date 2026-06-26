## Description: <br>
One MCP gateway to 230+ AI tools, including SEO, web search, image generation, video, screenshots, security scanning, and more, with auto-provisioning on first use and no API key setup required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blakefolgado](https://clawhub.ai/user/blakefolgado) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use ToolRouter to connect an agent to a broad MCP gateway for web search, SEO, media generation, screenshots, security scanning, company lookup, flight search, social media, financial data, and similar external tool workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables a broad external MCP gateway with many tool categories, which can expand the agent's action surface. <br>
Mitigation: Install it only when broad external tool access is intended, and require approval for paid calls, account-linked actions, sensitive data handling, and public posting or moderation workflows. <br>
Risk: The installation changes the user's OpenClaw MCP configuration and runs the toolrouter-mcp package through npx. <br>
Mitigation: Review the ~/.openclaw/openclaw.json change before saving it, and consider pinning or reviewing the npm package before use. <br>
Risk: Auto-provisioning and usage-based paid tools can create account and billing implications after first use. <br>
Mitigation: Confirm the claim and billing flow before using paid tools, and keep free and paid tool use subject to explicit user approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blakefolgado/toolrouter) <br>
- [ToolRouter Website](https://toolrouter.com) <br>
- [ToolRouter Tools Catalog](https://toolrouter.com/tools) <br>
- [ToolRouter Setup Guide](https://toolrouter.com/connect) <br>
- [toolrouter-mcp npm Package](https://www.npmjs.com/package/toolrouter-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration instructions, Shell commands, Guidance, API Calls] <br>
**Output Format:** [Markdown with JSON configuration, command examples, and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connects agents to a broad external MCP gateway; some tools may involve account-linked actions, sensitive data, or usage-based billing.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
