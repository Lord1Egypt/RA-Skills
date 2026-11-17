## Description:

Unified SaaS integration gateway via api.aisa.one (AISA gateway, v3.1): manage OAuth auth for third-party SaaS apps, tool execution, tool-router sessions, triggers, webhooks, MCP servers, and usage stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect third-party SaaS accounts, inspect gateway session state, execute SaaS tools, manage MCP access, configure triggers and webhooks, and review usage through the AISA gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad proxy execution and persistent MCP sessions can exercise connected-account privileges across third-party SaaS services.

Mitigation: Use the skill only when the user trusts AISA and confirms the exact account, destination, method, resource ID, and permitted tools before proxy execution or MCP creation.

Risk: OAuth links, tool execution, triggers, webhooks, MCP servers, project changes, and deletes can affect production data or automation.

Mitigation: Prefer read-only discovery first, confirm every state-changing POST, PATCH, or DELETE, and validate IDs and schemas from list or detail endpoints before execution.

Risk: Secrets and connected-account credentials may be exposed through prompts, shared logs, or overly broad project settings.

Mitigation: Avoid entering production secrets into prompts or logs, prefer explicit allowed_tools lists, and use gateway settings such as masked connected-account secrets, restricted log visibility, 2FA, and MCP API-key requirements where available.

## Reference(s):

- [Saas Gateway on ClawHub](https://clawhub.ai/bibaofeng/skills/saas-gateway)
- [AISA](https://aisa.one)
- [Agent Skills specification](https://agentskills.io/specification)
- [Composio documentation](https://docs.composio.dev)
- [Auth and session](references/auth_and_session.md)
- [Connect accounts](references/connect_account.md)
- [Execute tools](references/execute_tools.md)
- [MCP servers, projects, and usage](references/mcp_projects_usage.md)
- [AISA gateway endpoint catalog](references/endpoint_catalog.md)
- [Triggers and webhooks](references/triggers_webhooks.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, api calls, markdown]

**Output Format:** [Markdown guidance with curl examples, endpoint paths, configuration notes, and JSON request or response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and connected SaaS account context for live gateway operations.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
