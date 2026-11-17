## Description:

Use this skill for computer vision tasks including image recognition (OCR, object detection) and image generation (text-to-image, image-to-image). Supports asynchronous task execution with Tencent COS storage and Doubao AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgwanai](https://clawhub.ai/user/lgwanai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze local or remote images, extract text, answer image questions, and generate images from text or reference images. It is suited for document digitization, UI and content workflows, chart or table extraction, and accessibility descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local images, prompts, and results may be sent to Tencent COS and Doubao/Volcengine services.

Mitigation: Use the skill only when that cloud processing and retention posture is acceptable, and avoid sensitive documents unless retention and provider handling are approved.

Risk: Uploaded images may remain in the configured COS bucket after task completion.

Mitigation: Use a private COS bucket, restrict bucket access, and configure lifecycle deletion for uploaded task artifacts.

Risk: Local task file access and status lookups can create safety concerns if exposed to untrusted input.

Mitigation: Run the skill in a restricted environment and do not expose status commands to untrusted callers until task IDs are validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgwanai/skills/vision-skill)
- [Volcengine console](https://console.volcengine.com/)
- [Doubao Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI task JSON, text answers, Markdown or structured recognition output, and generated image URLs or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous tasks can be polled by task ID and may save text or image results to local output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
