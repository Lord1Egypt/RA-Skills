## Description:

小红书 helps agents search Xiaohongshu notes, inspect details and comments, browse recommended feeds, and publish image-text posts through a user-managed local MCP component.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to research Xiaohongshu content, review note details and comments, browse feeds, and prepare authorized image-text posts. Publishing requires a user-managed local MCP service and explicit per-post authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A non-local MCP endpoint override could send Xiaohongshu tokens or draft post content to a remote server.

Mitigation: Keep the endpoint on loopback by default, and do not set XHS_ALLOW_REMOTE=yes or XHS_MCP_BASE_URL to a non-loopback address unless the server is fully trusted.

Risk: The required third-party local MCP component can act through the configured Xiaohongshu account, including publishing public content.

Mitigation: Audit and pin the upstream component version, use a dedicated Xiaohongshu account, review each post before publishing, stop the component after use, and revoke the login device in the official app.

Risk: The maintainer publish script is unrelated to end-user Xiaohongshu posting and mutates ClawHub distribution state.

Mitigation: Normal users should not run scripts/publish.sh; reserve it for maintainers with the required ClawHub credentials and explicit publish confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wscats/skills/xhs-cn)
- [SETUP.md](SETUP.md)
- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
- [xiaohongshu-mcp Releases](https://github.com/xpzouying/xiaohongshu-mcp/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands interact with a user-managed local MCP service; publish operations require explicit authorization and a dedicated-account attestation.]

## Skill Version(s):

1.0.10 (source: server release evidence, released 2026-05-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
