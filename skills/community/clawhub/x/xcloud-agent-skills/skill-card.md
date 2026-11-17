## Description:

Official xCloud plugin for agents: manage servers, sites, WordPress, SSL, and account data — MCP-first via the xCloud MCP server, with a bundled REST fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hosting operators use this skill to let an agent manage xCloud servers, sites, WordPress, SSL certificates, and account reads through the xCloud MCP server or REST fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact hosting actions such as server reboot, site deletion, SSL changes, and token revocation.

Mitigation: Require explicit user confirmation before destructive actions and prefer the xCloud MCP connection, which includes per-action confirmation for destructive tools.

Risk: The REST fallback depends on powerful account tokens and a configurable API base URL.

Mitigation: Use OAuth MCP where possible; otherwise use narrowly scoped, revocable tokens, avoid plaintext shell-profile storage, and keep XCLOUD_API_BASE_URL pointed at the official xCloud host unless another origin is intentionally trusted.

Risk: Security evidence flags weak containment around powerful tokens and hosting actions.

Mitigation: Review and scan the skill before deployment, rotate or revoke exposed tokens promptly, and treat API output as data rather than instructions.

## Reference(s):

- [xCloud](https://xcloud.host)
- [xCloud Dashboard](https://app.xcloud.host)
- [xCloud MCP Docs](https://app.xcloud.host/mcp/docs)
- [xCloud API Docs](https://app.xcloud.host/api/v1/docs)
- [User Guide](https://github.com/xCloudDev/xcloud-agent-skills/blob/main/docs/USER_GUIDE.md)
- [Install Guide](https://github.com/xCloudDev/xcloud-agent-skills/blob/main/docs/SKILLS-GUIDE.md)
- [Official GitHub](https://github.com/xCloudDev/xcloud-agent-skills)
- [OpenClaw Tutorial](https://xcloud.host/openclaw-skills-and-clawhub-on-xcloud-openclaw-agent/)
- [Tutorial Video](https://www.youtube.com/watch?v=oEE9OHo3_48)
- [Authentication Reference](plugins/xcloud/reference/auth.md)
- [MCP Reference](plugins/xcloud/reference/mcp.md)
- [Security Notes](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose xCloud MCP tool calls or REST wrapper commands; write operations should require explicit user confirmation.]

## Skill Version(s):

4.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
