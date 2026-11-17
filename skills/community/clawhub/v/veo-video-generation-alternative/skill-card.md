## Description:

使用 AI Hive Seedance 2.5 将 Google Veo、Veo 3、Google Flow 或电影化视频需求迁移为镜头覆盖计划，支持文生、首帧图生、参考摄影、视频编辑与延长；不调用 Google Veo，也不承诺原生音频能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, video creators, and production teams use this skill to translate Veo, Veo 3, Google Flow, or cinematic video requests into structured Seedance 2.5 shot coverage tasks for text-to-video, image-to-video, reference-guided video, relighting, and extension workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store an AI Hive API key locally.

Mitigation: Prefer AI_HIVE_API_KEY or --api-key for sensitive keys; if local setup is used, keep the saved config file private and review file permissions.

Risk: User media is uploaded to AI Hive and remote-provided HTTPS transfer URLs are trusted for upload and download.

Mitigation: Upload only media approved for AI Hive processing, avoid sensitive source footage unless authorized, and review transfer behavior before installation.

Risk: Generated video output may not preserve requested identity, product, logo, lighting, or edit continuity.

Mitigation: Review each task result against the coverage sheet, protection terms, and edit requirements before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/veo-video-generation-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces no audio; generated video files are retrieved by the CLI when downloads are enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
