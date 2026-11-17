## Description:

企业微信 MCP 配置指南。当用户需要"添加企业微信"、"配置企微"、"启用企微消息"、"设置企业微信集成"时触发。提供完整的 MCP Server 配置、权限白名单设置和 Gateway 重启指引。

This skill is ready for commercial/non-commercial use.

## Publisher:

[stliuexp](https://clawhub.ai/user/stliuexp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to configure an OpenClaw MCP integration for WeCom, including server setup, tool allowlisting, Gateway restart, and basic verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned third-party `wecom-mcp-server` package.

Mitigation: Review the package source and publisher before use, then pin the MCP package to a reviewed exact version.

Risk: The MCP server uses WeCom enterprise credentials.

Mitigation: Use a least-privilege WeCom application, keep secrets in local configuration only, and rotate the WeCom secret if exposure is suspected.

Risk: The setup grants MCP tool access and restarts the Gateway.

Mitigation: Restrict the MCP process where possible and allow only the required `wecom_mcp` tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stliuexp/skills/wecom-mcp-setup)
- [Publisher profile](https://clawhub.ai/user/stliuexp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup prerequisites, MCP server configuration, allowlist commands, restart guidance, verification steps, troubleshooting, and security notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
