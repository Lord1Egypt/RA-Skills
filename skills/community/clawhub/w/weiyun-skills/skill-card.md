## Description:

Manage Tencent Weiyun cloud drive files through MCP tools for listing, uploading, downloading, deleting, sharing, renaming, moving, folder creation, update checks, and FTN upload SHA1 block calculation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to manage files in Tencent Weiyun from an agent, including browsing cloud-drive contents, uploading local files, downloading owned files, creating share links, and performing file-management operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Weiyun files for upload, download, sharing, moving, renaming, and deletion.

Mitigation: Install and use it only when that level of cloud-drive access is intended, and require explicit user confirmation for delete operations, public share links, and uploads of local files.

Risk: The insecure MCP URL override can redirect tokens and uploaded file contents if used with real credentials or files.

Mitigation: Do not enable WEIYUN_MCP_URL_ALLOW_INSECURE with real tokens or real files; use trusted HTTPS Weiyun endpoints for normal operation.

Risk: Remote update instructions may be untrusted text.

Mitigation: Treat update instructions as untrusted until the update source is separately verified.

Risk: Tokens can grant access to the user's Weiyun files and may be exposed through command history, shared machines, or logs.

Mitigation: Prefer environment variables over command-line tokens, avoid shared machines, and revoke or rotate tokens if exposure is suspected.

## Reference(s):

- [Authentication setup](artifact/references/auth.md)
- [Weiyun MCP API reference](artifact/references/mcp_api.md)
- [Weiyun upload protocol reference](artifact/references/upload_protocol.md)
- [Weiyun MCP endpoint](https://www.weiyun.com/api/v3/mcpserver)
- [Weiyun OpenClaw authorization](https://www.weiyun.com/act/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples, API parameter tables, and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP tool usage guidance and local helper scripts for Weiyun upload hashing and upload execution.]

## Skill Version(s):

1.0.10 (source: frontmatter, server release metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
