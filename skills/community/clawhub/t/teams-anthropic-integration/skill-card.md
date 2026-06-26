## Description: <br>
Use @youdotcom-oss/teams-anthropic to add Anthropic Claude models (Opus, Sonnet, Haiku) to Microsoft Teams.ai applications, with optional You.com MCP server integration for web search and content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdwardIrby](https://clawhub.ai/user/EdwardIrby) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add Anthropic Claude chat, streaming, function calling, and optional You.com MCP web search capabilities to Microsoft Teams.ai applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Teams app messages, search queries, URLs, and retrieved web content may be processed by Anthropic and You.com when the integration is used. <br>
Mitigation: Install and enable the skill only where organizational policy permits those external services, and scope or disable You.com MCP tools for sensitive internal environments. <br>
Risk: Anthropic and You.com API keys are required for the documented setup paths. <br>
Mitigation: Store API keys in environment variables or a managed secret store, keep them out of source control, and pin package versions with a lockfile. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EdwardIrby/teams-anthropic-integration) <br>
- [@youdotcom-oss/teams-anthropic package source](https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/teams-anthropic) <br>
- [You.com MCP server documentation](https://documentation.you.com/developer-resources/mcp-server) <br>
- [Anthropic Console](https://console.anthropic.com/) <br>
- [You.com API keys](https://you.com/platform/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes npm install commands, environment variable names, Teams.ai code templates, model-selection guidance, and validation checklists.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
