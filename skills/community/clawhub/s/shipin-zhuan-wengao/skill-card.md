## Description:

将本地 MP4 文件或可直接下载的 MP4 链接转写为精炼文本，并可按提示词生成总结、改写、金句提取或翻译。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、会议记录人员和学习者可用它从已完成的 MP4 视频中提取发言，并整理成转写稿、摘要、会议纪要、改写文案或翻译。使用前需要配置服务令牌；服务按量或按套餐计费。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flagged an undisclosed third-party token promotion.

Mitigation: Confirm why GUAIKEI_API_TOKEN is required and review the service terms before providing a token; keep the token out of command text and logs.

Risk: Only 9 of 20 components were fully inspected, leaving behavior uncertain.

Mitigation: Review the remaining components and complete a full security scan before installation.

## Reference(s):

- [视频转文稿服务](https://www.guaikei.com)
- [Release changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown, depending on the prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one MP4 video per command; output may be a transcription or prompt-directed content.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
