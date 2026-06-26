## Description: <br>
Tencent Drive(Weiyun) MCP helps agents use Weiyun MCP tools for cloud file listing, category search, downloads, uploads, sharing, renaming, folder creation, moves, deletes, and upload hash preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun-percy](https://clawhub.ai/user/yun-percy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage files in Tencent Weiyun through MCP, including browsing, upload preparation, upload execution, downloads, sharing, renames, moves, and deletion workflows. It is most useful when an agent needs precise Weiyun tool arguments or local SHA1 block metadata for FTN upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent delegated access to manage Weiyun cloud files, including uploads, downloads, moves, renames, deletes, permanent deletes, and share-link creation. <br>
Mitigation: Require explicit user confirmation before any file-changing action, local download, permanent deletion, or share-link creation. <br>
Risk: The skill handles MCP tokens, Weiyun cookies, download cookies, and share links that can expose account access or private files. <br>
Mitigation: Treat tokens, cookies, and share links as secrets; avoid logging them and keep the MCP URL on the official Weiyun endpoint. <br>
Risk: The artifact includes helper scripts for local upload workflows. <br>
Mitigation: Inspect setup or helper scripts before running them and only execute commands needed for the specific user-approved task. <br>


## Reference(s): <br>
- [Weiyun authentication reference](references/auth.md) <br>
- [Weiyun MCP API reference](references/mcp_api.md) <br>
- [Weiyun upload protocol reference](references/upload_protocol.md) <br>
- [Weiyun MCP server endpoint](https://www.weiyun.com/api/v3/mcpserver) <br>
- [Weiyun OpenClaw authorization page](https://www.weiyun.com/act/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/yun-percy/tencent-drive-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, MCP call arguments, Python script usage, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions and local upload metadata; can guide actions that affect cloud files.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
