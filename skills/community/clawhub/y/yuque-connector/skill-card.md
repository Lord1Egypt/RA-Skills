## Description:

语雀连接器 helps agents synchronize Yuque knowledge bases with local files by importing common document formats and downloading Yuque documents as local Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuwu2495](https://clawhub.ai/user/jiuwu2495)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to move documents between local workspaces and Yuque knowledge bases, including bulk imports, downloads, directory organization, search, and updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a read/write Yuque token and stores it in local MCP configuration.

Mitigation: Use a least-privilege Yuque token when possible, avoid long-lived tokens in chat, and rotate or revoke tokens after use.

Risk: The skill rewrites shared MCP configuration at ~/.workbuddy/mcp.json.

Mitigation: Inspect the configuration change before use, keep file permissions restricted, and retain backups only where they do not expose secrets.

Risk: The skill runs an unpinned npm connector for Yuque MCP access.

Mitigation: Prefer a pinned, reviewed yuque-mcp version before installing or running the connector in sensitive environments.

Risk: Bulk import, update, and download operations can affect many Yuque documents.

Mitigation: Confirm repository IDs, document scopes, and synchronization direction before bulk actions, especially when write access is enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiuwu2495/skills/yuque-connector)
- [Yuque MCP Server](https://github.com/yuque/yuque-mcp-server)
- [Yuque API v2](https://www.yuque.com/api/v2)
- [Yuque Token Settings](https://www.yuque.com/settings/tokens)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text responses with file paths, Yuque document links, JSON configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local Markdown files, Yuque document links, MCP configuration guidance, and retry or recovery steps.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
