## Description:

从小红书、抖音、快手、微博和视频号的公开视频链接、分享文案、内容 ID 或已有任务中提取视频信息、简介和口播逐字稿，并整理为可复制或精简文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向短视频创作者及需要整理视频内容的用户，提取受支持平台的公开视频信息和口播逐字稿，并整理成可复制文案或摘要。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI is invoked without a fixed version, so a later release could change how it handles credentials.

Mitigation: Review the CLI release and pin an approved version before use; keep credentials in the intended private environment and never include them in prompts or output.

Risk: Submitted video links or share text may be sent to SocialDataX for processing.

Mitigation: Submit only content you are authorized to share with the service, and review the requested input before sending it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-short-video-copy-extract)
- [SocialDataX API Key and skill information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with video details, source description, transcript, copy-ready text, concise summary, or task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform- and task-dependent; reports only fields returned by the service and continues pending tasks by job ID.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
