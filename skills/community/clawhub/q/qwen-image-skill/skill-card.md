## Description:

Generate images using Alibaba Cloud Bailian Qwen-Image and Z-Image models (通义千图文生图 + 人像照片模型).

This skill is ready for commercial/non-commercial use.

## Publisher:

[irron](https://clawhub.ai/user/irron)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate image files from text prompts with automatic model selection for portrait/photo prompts versus general image-generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read DASHSCOPE_API_KEY from local TOOLS.md files, which may expose or reuse credentials outside a controlled environment.

Mitigation: Provide DASHSCOPE_API_KEY through a controlled environment variable and avoid storing the key in shared TOOLS.md files.

Risk: Image prompts are sent to Alibaba Cloud DashScope for processing.

Mitigation: Do not submit sensitive prompts unless external processing by Alibaba Cloud is acceptable for the use case.

Risk: The image download path saves API-provided URLs without sufficient host, response, or size validation.

Mitigation: Review the skill before deployment and add allowed-host, response status, content type, and maximum-size checks for downloaded images.

## Reference(s):

- [Qwen-Image API documentation](https://help.aliyun.com/zh/model-studio/qwen-image-api)
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [Image file output with console status text and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; supports prompt, model, size, prompt extension, watermark, and output-path options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
