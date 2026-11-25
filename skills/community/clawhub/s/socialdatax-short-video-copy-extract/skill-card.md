## Description:

从小红书、抖音、快手、微博和视频号的公开视频链接、分享文案、内容 ID 或已有任务中提取视频信息与口播逐字稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要整理短视频内容的用户和代理，提交支持平台的视频链接、分享文案或内容 ID，获取视频基础信息、简介和口播逐字稿，并整理为可复制文案或精简版。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands that run a changeable latest CLI package version create a supply chain risk.

Mitigation: Use an exact reviewed package version with verified integrity before running commands.

Risk: Some CLI calls run in environments where API credentials are used, and scanner coverage for this release was partial.

Mitigation: Keep credentials in the intended private environment, do not expose them in messages or command arguments, and review unresolved local references before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-short-video-copy-extract)
- [SocialDataX API key and service information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown summaries and transcripts, JSON task responses, and optional UTF-8 SRT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only report fields present in the task response; provide a transcript only after successful completion. SRT export is optional and requires a user-requested new file path.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
