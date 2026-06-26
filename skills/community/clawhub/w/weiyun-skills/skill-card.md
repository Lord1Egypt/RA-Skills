## Description: <br>
Manage Tencent Weiyun cloud-drive files through MCP tools for listing, uploading, downloading, deleting, sharing, renaming, moving, and creating folders, with local FTN upload hash calculation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage files in a Tencent Weiyun cloud drive from an agent, including browsing, upload and download workflows, share-link generation, folder operations, and upload parameter calculation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weiyun MCP tokens and download cookies can grant access to user cloud-drive data. <br>
Mitigation: Prefer environment variables or mcporter configuration, avoid echoing tokens in chat or shell history, and remove stored credentials from temporary or shared devices after use. <br>
Risk: Delete and permanent-delete operations can remove user files or folders, with permanent deletion bypassing recovery. <br>
Mitigation: Require explicit user confirmation, echo the exact target names and counts before acting, default to recycle-bin deletion, and require a second confirmation for permanent deletion or directory deletion. <br>
Risk: Generated share links can expose private files or folders to anyone with the link. <br>
Mitigation: Confirm the sharing intent and target list before generating links, state the visibility implications, and use a password unless the user explicitly asks for an unprotected link. <br>
Risk: The upload helper reads local file contents and sends them to the configured Weiyun MCP endpoint. <br>
Mitigation: Confirm exact local paths before uploads and keep the MCP endpoint restricted to trusted Weiyun or QQ hosts unless a user explicitly enables local debugging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/weiyun-skills) <br>
- [Weiyun authentication guide](references/auth.md) <br>
- [Weiyun MCP API reference](references/mcp_api.md) <br>
- [Weiyun upload protocol reference](references/upload_protocol.md) <br>
- [Weiyun MCP server endpoint](https://www.weiyun.com/api/v3/mcpserver) <br>
- [Weiyun authorization page](https://www.weiyun.com/act/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code, API calls] <br>
**Output Format:** [Markdown instructions with inline shell commands, MCP tool call guidance, and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local upload parameters such as block_sha_list, file_sha, check_sha, and check_data for Weiyun upload workflows.] <br>

## Skill Version(s): <br>
1.0.10 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
