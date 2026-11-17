## Description:

指导代理使用 ffmpeg 将本地视频或经 qhkit 解析的分享链接中的音轨导出为 MP3 或 WAV。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和开发者可用它从本地视频或平台分享链接提取音轨，用于编辑或内容制作。人声与伴奏分离不在其能力范围内。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing ffmpeg or qhkit may change the local environment, including a global npm installation.

Mitigation: Ask before installing dependencies and confirm the package source and installation scope.

Risk: qhkit setup may replace an existing regional configuration without the user's choice.

Mitigation: Check the current configuration and ask before changing the selected site or environment.

Risk: Configuring qhkit with an API key and submitting platform links to Qinghu may expose credentials or video links to an external service.

Mitigation: Explain the external service use, obtain consent, and prefer a scoped temporary key instead of sharing a long-lived or privileged key with the agent.

Risk: Extracted background music may be subject to copyright restrictions for commercial reuse.

Mitigation: Remind users to confirm rights before using extracted music commercially.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-video-audio-extract)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎AI 工作台 API Keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides the extracted MP3/WAV file path; may also provide a video script or send the audio file when supported.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
