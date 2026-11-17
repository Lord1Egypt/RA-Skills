## Description:

Tencent Drive(Weiyun) MCP guides agents through Weiyun cloud-drive file management over MCP, including listing, upload, download, delete, sharing, rename, create, move, and upload hash calculation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun-percy](https://clawhub.ai/user/yun-percy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate Tencent Weiyun cloud storage through MCP, including browsing files, uploading and downloading content, creating share links, and moving or deleting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud-file management tools can upload, delete, move, rename, and share files in the user's Weiyun account.

Mitigation: Require explicit confirmation of the exact files, directories, destinations, sharing settings, and deletion mode before taking action.

Risk: MCP tokens, cookies, download URLs, and share links can grant access to cloud files.

Mitigation: Treat these values as sensitive, prefer configured secrets or environment variables over command-line tokens, and avoid exposing them in prompts, logs, or shell history.

Risk: Update and setup guidance can lead the agent to execute scripts or follow remote update instructions.

Mitigation: Verify script paths and review returned update instructions before execution; do not follow remote update instructions automatically.

Risk: Uploads and downloads operate on local file paths and remote cloud locations selected by the agent.

Mitigation: Confirm the source file, target directory, and download destination with the user before transferring data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yun-percy/skills/tencent-drive-mcp)
- [Weiyun MCP API Reference](references/mcp_api.md)
- [Weiyun Authentication Reference](references/auth.md)
- [Weiyun Upload Protocol Reference](references/upload_protocol.md)
- [Weiyun MCP Server Endpoint](https://www.weiyun.com/api/v3/mcpserver)
- [Weiyun OpenClaw Authorization](https://www.weiyun.com/act/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP tool call guidance, token configuration steps, and local SHA1 block calculation/upload scripts.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
