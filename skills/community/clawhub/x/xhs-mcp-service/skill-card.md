## Description:

Xhs Mcp Service provides a local MCP service for automating Xiaohongshu/RED account actions such as login checks, content search, engagement, comments, and image or video publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackydai-bc](https://clawhub.ai/user/jackydai-bc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to a local Xiaohongshu MCP service for account automation workflows, including search, profile lookup, engagement actions, comments, and publishing after manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local service can control a real Xiaohongshu account, including publishing, commenting, liking, favoriting, and uploading local files.

Mitigation: Require manual review before any account-changing action or upload, and limit use to trusted operators.

Risk: Weak local-network controls could expose the MCP service beyond the intended machine.

Mitigation: Bind the service to localhost and add authentication, firewall isolation, or equivalent network restrictions.

Risk: Stored cookies can grant account access if exposed.

Mitigation: Keep cookies.json private, restrict filesystem permissions, rotate login state when needed, and avoid running the service as admin or root.

## Reference(s):

- [Xhs Mcp Service on ClawHub](https://clawhub.ai/jackydai-bc/skills/xhs-mcp-service)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Puppeteer documentation](https://pptr.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and JavaScript examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands or scripts that control a real Xiaohongshu account through a local MCP service.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
