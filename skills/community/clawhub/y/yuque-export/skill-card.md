## Description:

通过 Chrome DevTools MCP 使用已登录的浏览器会话，将语雀知识库文档导出为保留目录结构的本地 Markdown 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sh1-5](https://clawhub.ai/user/sh1-5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to export authenticated Yuque knowledge bases into local Markdown archives. It is useful when preserving Yuque folder structure and optionally localizing referenced images for offline review or migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes authenticated Yuque knowledge-base content through the agent.

Mitigation: Use it only for Yuque repositories whose contents are appropriate for agent processing.

Risk: The skill writes exported Markdown files to a local destination.

Mitigation: Export to a dedicated folder and review the destination before running.

Risk: The --images option downloads remote Yuque CDN assets into local storage.

Mitigation: Enable --images only when local image copies are desired, then review the generated _assets folder.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and concise progress or completion text, with optional shell commands for local file and asset handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local directory tree under the selected output path and may create an _assets folder when image download is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
