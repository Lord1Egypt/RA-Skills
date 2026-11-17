## Description:

使用 AI Hive Seedance 2.5 将 Runway、Runway AI、Gen-4 或生成式视频制作需求迁移为可追踪的镜头版本，支持文生、首帧图生、参考素材、视频编辑与延长。Use when users search Runway 替代、Runway 平替、Gen-4 alternative、Runway API、AI 电影镜头、广告视频、生成式编辑、扩镜或视频延长；不访问 Runway 项目，也不表示技术兼容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and video production teams use this skill to plan tracked AI video shots and run AI Hive Seedance 2.5 text-to-video, image-to-video, reference-to-video, edit, and extend tasks as an alternative workflow to Runway-style generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, customer, or unreleased media may be uploaded to AI Hive or server-provided storage URLs during generation.

Mitigation: Review the skill before installing, use a constrained environment, use a limited AI Hive API key, and avoid private or unreleased media unless approved.

Risk: Generated media is downloaded locally by default.

Mitigation: Use a controlled output directory or the no-download mode when local retention is not desired, and review downloaded files before sharing.

Risk: Upload and download destinations and sizes depend on server-provided responses.

Mitigation: Verify service domain behavior, restrict network egress where practical, and check media size and source authorization before upload or download.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/runway-video-generation-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can submit API calls, upload local media, poll task status, and download generated media to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
