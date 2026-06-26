## Description: <br>
Configure OpenClaw to use Z.AI GLM Coding Plan models, region-specific endpoints, model settings, and optional Z.AI MCP tools for coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelmaz](https://clawhub.ai/user/nelmaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw for Z.AI GLM Coding Plan models, select the appropriate region and model, validate gateway setup, and optionally add Z.AI MCP tools for coding research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or bearer tokens may be exposed through shell history or local OpenClaw configuration files. <br>
Mitigation: Use a dedicated API key, avoid pasting real bearer tokens into shell commands, and protect ~/.openclaw/openclaw.json. <br>
Risk: Coding requests and optional MCP tool use route content to Z.AI services. <br>
Mitigation: Use the provider and MCP tools only when third-party use is approved, and avoid sending secrets, proprietary code, regulated data, or customer information unless that use is authorized. <br>


## Reference(s): <br>
- [Z.AI Coding Plan](https://z.ai/subscribe) <br>
- [OpenClaw Z.AI Provider](https://docs.openclaw.ai/providers/zai) <br>
- [GLM Models Overview](https://docs.openclaw.ai/providers/glm) <br>
- [Web Search MCP](https://docs.z.ai/devpack/mcp/search-mcp-server) <br>
- [Web Reader MCP](https://docs.z.ai/devpack/mcp/reader-mcp-server) <br>
- [Zread MCP](https://docs.z.ai/devpack/mcp/zread-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include region-specific endpoint choices, model recommendations, and MCP setup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
