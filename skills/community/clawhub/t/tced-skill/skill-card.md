## Description:

TCED Cloud Drive integrates Tencent Cloud Enterprise Drive with MCP tools so agents can authenticate with OAuth2 and manage files, accounts, and personal or team storage spaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuijiawei123](https://clawhub.ai/user/cuijiawei123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise users use this skill to connect an agent to Tencent Cloud Enterprise Drive, complete OAuth2 authorization, and perform cloud drive file, account, and space management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server can access Tencent Cloud Enterprise Drive content after OAuth authorization.

Mitigation: Install and authorize it only for accounts and spaces where agent-based cloud drive access is intended.

Risk: OAuth access and refresh tokens are stored in ~/.tced-mcp/auth.json.

Mitigation: Protect the credentials file with owner-only permissions and avoid sharing or committing it.

Risk: Misconfigured TCED_PAN_DOMAIN or TCED_BASE_PATH values could send token-bearing requests to untrusted endpoints.

Mitigation: Keep both environment variables pinned to the official Tencent endpoints documented by the skill.

Risk: Using an unpinned npm package version can increase supply-chain exposure.

Mitigation: Pin tced-mcp to the documented version and verify package source or changelog before upgrading.

## Reference(s):

- [TCED MCP Server API Reference](references/api_reference.md)
- [Tencent Cloud Enterprise Drive authorization page](https://pan.tencent.com)
- [Tencent Cloud Enterprise Drive API endpoint](https://api.tencentsmh.cn)
- [ClawHub skill page](https://clawhub.ai/cuijiawei123/skills/tced-skill)
- [Publisher profile](https://clawhub.ai/user/cuijiawei123)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline JSON configuration and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP tool calls that upload, download, list, search, or inspect cloud drive files after OAuth authorization.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
