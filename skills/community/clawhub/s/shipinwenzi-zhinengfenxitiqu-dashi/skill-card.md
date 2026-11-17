## Description:

将视频内容转写为文本。支持网络视频链接和本地视频文件两种输入，调用千问大模型进行语义解析，自动剔除语气词、口误、重复台词等无效内容，并支持按指定风格生成文案。适用于短视频二次创作、企业会议纪要、线上课程拆解、直播复盘、人物采访整理、知识素材提取、探店脚本撰写、培训课件整理等场景。当用户需要把视频转成文字、提取视频语音内容、生成视频文案或会议纪要时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、会议组织者和需要整理视频资料的团队，可将本地 MP4 或可直接下载的 MP4 链接转为文字，并按提示词生成摘要、改写、翻译或会议纪要。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a mismatch involving the token requirement and third-party promotion relative to the stated transcription purpose.

Mitigation: Verify the GUAIKEI_API_TOKEN source and service terms before use.

Risk: The security review notes cleanup concerns and partial code inspection.

Mitigation: Check cleanup behavior first and avoid using the skill with files you cannot afford to lose.

## Reference(s):

- [更新日志](references/changelog.md)
- [GuaiKei 官网](https://www.guaikei.com)
- [项目仓库](https://github.com/um-why/video2text-skill)
- [项目问题跟踪](https://github.com/um-why/video2text-skill/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown prose, based on the requested prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one video per run; a prompt can request transcription, summarization, rewriting, extraction, or translation.]

## Skill Version(s):

1.1.1 (source: artifact/SKILL.md frontmatter, artifact/package.json, artifact/references/changelog.md; released 2026-11-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
