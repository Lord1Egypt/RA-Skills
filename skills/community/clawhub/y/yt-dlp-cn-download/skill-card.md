## Description:

指导用户在中国大陆网络环境下配置 yt-dlp 下载视频，并排查代理、格式、认证和 Windows GUI 相关问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

在中国大陆网络环境下下载视频的用户和开发者，可用此技能配置 yt-dlp、排查下载故障，以及选择视频格式与批量下载参数。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 技能建议关闭宿主环境的文件删除保护，可能绕过清理操作的安全确认。

Mitigation: 不要关闭删除保护；优先使用 -k 保留中间文件，在专用下载目录中操作，并明确批准后续清理。

Risk: 浏览器 Cookie 或明文 cookies.txt 包含敏感的登录凭据。

Mitigation: 仅在确有需要时使用 Cookie，妥善限制明文文件访问，不要分享或上传。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/yt-dlp-cn-download)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes yt-dlp command options and Windows GUI implementation guidance.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
