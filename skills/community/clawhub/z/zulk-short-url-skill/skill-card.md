## Description: <br>
Premium AI-first URL shortening and management with real-time analytics and team collaboration via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentmilindu](https://clawhub.ai/user/agentmilindu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and operations teams use this skill to let an agent create and manage Zu.lk short links, inspect analytics, and manage organization membership through the Zu.lk MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change organization links, analytics, and membership after OAuth sign-in. <br>
Mitigation: Install only when Zu.lk is trusted for the relevant link and organization data, and use the intended Google or Zu.lk account for authentication. <br>
Risk: Link destination changes, member changes, or ADMIN/OWNER role grants can affect organization assets and access. <br>
Mitigation: Require explicit user confirmation before changing link destinations, adding or removing members, or granting ADMIN/OWNER roles. <br>
Risk: Using a bridge command for MCP transport may add unnecessary local execution surface compared with direct HTTPS configuration. <br>
Mitigation: Prefer the direct HTTPS MCP configuration when the client supports it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentmilindu/zulk-short-url-skill) <br>
- [Zu.lk MCP Endpoint](https://mcp.zu.lk/mcp) <br>
- [Zu.lk SSE Endpoint](https://mcp.zu.lk/sse) <br>
- [Zu.lk MCP Documentation](https://zu.lk/-/mcp) <br>
- [Zu.lk API Documentation](https://zu.lk/-/api) <br>
- [Source Repository Metadata](https://github.com/Zu-lk/zulk-short-url-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration examples and natural-language summaries of MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an MCP-compatible client, internet access, and user OAuth authentication for Zu.lk account access.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
