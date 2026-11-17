## Description:

企业微信聊天文件获取 - 从 ~/.openclaw/media/inbound/ 目录检测和获取通过聊天传递的文件；当用户提到获取文件、发送文件、附件等请求时激活。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to locate, inspect, and archive files received through WeCom chat from the local inbound attachment directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may list, read, or copy local WeCom inbound attachments without a clearly scoped file request.

Mitigation: Require a specific current attachment or filename, confirm before opening or copying files, and avoid selecting files only by recency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chongjie-ran/skills/wecom-file-detect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and file-handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify, read, and copy local WeCom inbound attachments when invoked by user file requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
