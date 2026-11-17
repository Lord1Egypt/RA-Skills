## Description:

Qwen Video Generator turns text prompts into short videos using Alibaba Cloud DashScope's wan2.2-t2v-plus model, with configurable resolution, duration, and prompt extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imnull](https://clawhub.ai/user/imnull)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create short video files from text prompts, choosing resolution, duration, model, and prompt-extension settings for Qwen/DashScope video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Alibaba Cloud DashScope.

Mitigation: Use a dedicated DashScope key with limited scope where possible, and avoid secrets or sensitive personal data in prompts.

Risk: The skill downloads provider-supplied video URLs and stores generated videos locally without strong network or size controls.

Mitigation: Set a controlled output directory and review or patch the download code before using the skill in sensitive or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imnull/skills/qwen-video-generator)
- [DashScope video synthesis endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis)
- [DashScope task status endpoint](https://dashscope.aliyuncs.com/api/v1/tasks/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands and a local MP4 video path when generation succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DashScope API key; generated video files are saved under VIDEO_OUTPUT_DIR or workspace/videos and reported as VIDEO_PATH:<path>.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
