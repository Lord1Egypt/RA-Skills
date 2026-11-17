## Description:

使用 AI Hive Seedance 2.5 将 Sora、OpenAI Sora 或长提示视频概念迁移为世界状态与物理连续性明确的短镜头，覆盖文生、首帧图生、参考素材、视频编辑和延长。Use when users search Sora 替代、Sora 平替、OpenAI video alternative、Sora API、长提示视频、世界模拟、电影镜头、广告短片或视频编辑；不是 OpenAI Sora 接口。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to convert Sora-style video ideas into AI Hive Seedance 2.5 world-state prompts and CLI workflows for text-to-video, image-to-video, reference-guided generation, video repair, and extension.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected image or video files are sent to AI Hive for generation, editing, extension, and task lookup.

Mitigation: Install and run the skill only when AI Hive Seedance 2.5 is the intended service and uploaded media is approved for that service.

Risk: Passing an API key on a visible command line can expose the secret in shell history or process listings.

Mitigation: Prefer a safer secret mechanism such as the AI_HIVE_API_KEY environment variable or a protected local config file.

Risk: The CLI depends on the requests package and the artifact does not pin dependency versions.

Mitigation: Use a virtual environment with pinned dependencies before operational use.

Risk: Generated MP4 files download to the default Downloads/AiHive location unless configured otherwise.

Mitigation: Use --output-dir to choose an appropriate location or --no-download when only the task ID is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/sora-video-generation-alternative)
- [AI Hive OpenAPI endpoint used by the skill](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with bash command examples; the bundled CLI emits task IDs, JSON status, media upload IDs, and downloaded MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and may upload selected images or videos to AI Hive.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
