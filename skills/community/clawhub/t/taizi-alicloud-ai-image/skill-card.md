## Description:

Generate images with Model Studio DashScope SDK using Qwen Image generation models (qwen-image-max, qwen-image-plus-2026-01-09). Use when implementing or documenting image.generate requests/responses, mapping prompt/negative_prompt/size/seed/reference_image, or integrating image generation into the video-agent pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to standardize Qwen Image generation requests and responses through Alibaba Cloud Model Studio DashScope. It helps agents map prompt, negative prompt, size, seed, style, and reference image inputs into generated image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images can be read from arbitrary local paths and uploaded to DashScope.

Mitigation: Use only approved input directories, validate image file types, and avoid sensitive prompts or reference images.

Risk: The release does not clearly disclose reference-image uploads to DashScope.

Mitigation: Disclose external processing before use and require user confirmation for reference-image uploads.

Risk: The DashScope dependency is installed at runtime without a pinned version in the skill instructions.

Mitigation: Pin and review the DashScope package before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fresh3/skills/taizi-alicloud-ai-image)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON examples, Python code, shell commands, and generated image files from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DashScope API key; helper output can include a saved image file, normalized JSON response, or base64 image data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
