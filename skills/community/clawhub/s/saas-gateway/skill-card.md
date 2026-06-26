## Description: <br>
Saas Gateway helps agents connect third-party SaaS accounts through api.aisa.one, manage OAuth sessions, execute tools, configure triggers and webhooks, manage MCP servers, and review usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect and operate third-party SaaS integrations through the AISA gateway, including account authorization, tool execution, automation triggers, MCP server setup, and usage review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect connected third-party SaaS accounts and sensitive gateway resources. <br>
Mitigation: Use least-privilege accounts and scopes, prefer OAuth and scoped tools, and require explicit user confirmation before mutating actions. <br>
Risk: Secrets or connected-account credentials may be exposed through chats, logs, raw proxy requests, or broad tool access. <br>
Mitigation: Do not paste secrets into chats or logs, avoid raw proxy requests unless necessary, and restrict MCP sessions and tool permissions to the minimum needed. <br>


## Reference(s): <br>
- [Auth and session](references/auth_and_session.md) <br>
- [Connect accounts](references/connect_account.md) <br>
- [Execute tools](references/execute_tools.md) <br>
- [Triggers and webhooks](references/triggers_webhooks.md) <br>
- [MCP servers, projects, and usage](references/mcp_projects_usage.md) <br>
- [Endpoint catalog](references/endpoint_catalog.md) <br>
- [AISA](https://aisa.one) <br>
- [Composio documentation](https://docs.composio.dev) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and user confirmation before write, delete, webhook, MCP, file, project, key-rotation, or SaaS tool-execution actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
