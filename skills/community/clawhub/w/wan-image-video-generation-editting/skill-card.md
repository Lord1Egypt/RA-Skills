## Description:

Generates and edits images and videos with Alibaba Wan models through DashScope API commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisyejh](https://clawhub.ai/user/krisyejh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative automation users use this skill to call Wan image and video generation, image editing, image-to-video, and reference-to-video workflows from an agent-managed CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, referenced URLs, and explicitly provided local image files are sent to Alibaba DashScope.

Mitigation: Use only media and prompts approved for upload to DashScope, and avoid private or confidential inputs unless policy permits that transfer.

Risk: Image and video generation requests can incur usage costs, especially with larger sizes, longer durations, or repeated polling workflows.

Mitigation: Review size, duration, and quantity options before execution, and use an approved DashScope API key with appropriate account controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krisyejh/skills/wan-image-video-generation-editting)
- [Alibaba ModelStudio Model Market](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)
- [Text-to-Image API Reference](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
- [Image Editing API Reference](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference)
- [Text-to-Video API Reference](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)
- [Image-to-Video API Reference](https://help.aliyun.com/zh/model-studio/image-to-video-api-reference)
- [Reference-to-Video API Reference](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)
- [wan2.6-t2i-api-doc.md](references/wan2.6-t2i-api-doc.md)
- [wan2.6-image-api-doc.md](references/wan2.6-image-api-doc.md)
- [wan2.6-t2v-api-doc.md](references/wan2.6-t2v-api-doc.md)
- [wan2.6-i2v-api-doc.md](references/wan2.6-i2v-api-doc.md)
- [wan2.6-r2v-api-doc.md](references/wan2.6-r2v-api-doc.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline bash commands and CLI output containing task IDs, media URLs, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and DASHSCOPE_API_KEY; generated media and task results are returned by the DashScope Wan API.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
