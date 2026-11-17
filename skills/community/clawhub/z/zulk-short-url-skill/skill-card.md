## Description:

Premium AI-first URL shortening and management with real-time analytics and team collaboration via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmilindu](https://clawhub.ai/user/agentmilindu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing teams use this skill to configure an MCP-enabled agent for creating short links, managing organizations and team members, and reviewing link analytics in Zu.lk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an unpinned npx stdio bridge option for connecting to the remote MCP server.

Mitigation: Use the HTTP MCP configuration when possible and review any local bridge command before running it.

Risk: Connected agents may read or modify links, analytics, organizations, and team membership for the authenticated account or organization.

Mitigation: Authenticate only with an account and organization whose Zu.lk permissions match the intended task, and review admin or owner role actions before approval.

## Reference(s):

- [Zulk skill page](https://clawhub.ai/agentmilindu/skills/zulk-short-url-skill)
- [Zu.lk website](https://zu.lk)
- [Zu.lk MCP documentation](https://zu.lk/-/mcp)
- [Zu.lk API documentation](https://zu.lk/-/api)
- [Zulk Short URL Skill repository](https://github.com/Zu-lk/zulk-short-url-skill)
- [Zulk MCP HTTP endpoint](https://mcp.zu.lk/mcp)
- [Zulk MCP SSE endpoint](https://mcp.zu.lk/sse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with JSON configuration examples, MCP tool calls, and concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an MCP-compatible client, internet access, and Zu.lk OAuth authentication.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
