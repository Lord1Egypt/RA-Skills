## Description:

把视频变成能直接用的文字。千问大模型驱动，粘贴链接或上传文件即可转写，自动过滤语气词、口误与重复内容，输出干净稿。无论是短视频二创改脚本、会议出纪要、课程拆知识点，还是直播复盘、采访整理，都能按你想要的风格一键成文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户、内容创作者和开发者可将本地 MP4 或可直接下载的 MP4 直链转成清理后的文稿，并按提示生成总结、改写、金句、分镜或翻译。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial; some behavior remains unverified, including environment-variable access and temporary-file cleanup.

Mitigation: Review token handling and temporary-file cleanup for your environment, and configure GUAIKEI_API_TOKEN securely before processing videos.

## Reference(s):

- [视频文本提取分析服务](https://www.guaikei.com)
- [ClawHub release](https://clawhub.ai/engheng-art/skills/shipinwenben-tiqufenxi)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Release changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown text returned on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription or prompt-directed summaries, rewrites, quotations, storyboards, and translations; processes one MP4 at a time and accepts prompts up to 1,000 characters.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
