## Description:

从 B 站、YouTube 等视频网站下载视频或音频，再用 MarkItDown 在本机转写成 Markdown。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hommertemp](https://clawhub.ai/user/hommertemp)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要整理在线视频内容的用户：下载有权访问的视频或音频，并生成可检索的 Markdown 转写稿。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 登录密码或带有秘密的链接可能出现在日志中。

Mitigation: 修复日志脱敏前，避免使用密码参数和包含秘密的链接；将日志与回执保存在私密位置。

Risk: 浏览器 Cookie 和导出的 Cookie 文件包含敏感登录凭据。

Mitigation: 仅在用户明确同意后访问浏览器 Cookie；使用专用浏览器配置，并妥善保护 Cookie 导出文件。

## Reference(s):

- [站点说明](references/sites.md)
- [故障排查](references/troubleshooting.md)
- [yt-dlp Cookie 常见问题](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [本地视频或音频文件、Markdown 转写稿及命令行使用说明]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [本机处理；可处理单个视频或播放列表，并支持仅下载音频。]

## Skill Version(s):

1.0.0 (source: skill frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
