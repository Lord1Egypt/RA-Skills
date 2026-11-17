## Description:

阿里云千问文生图模型（Qwen-Image）技能，支持图像生成，可根据中英文提示词调用 DashScope 千问图像模型并配置尺寸、数量、提示词扩展、水印和随机种子等参数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanlan314](https://clawhub.ai/user/lanlan314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate images with Alibaba Cloud DashScope Qwen-Image models from text prompts. It provides request examples, supported models, image size options, response parsing guidance, and common error handling notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unsafe shell-based prompt handling that could allow crafted prompts to run local commands.

Mitigation: Review before installing, use only non-sensitive prompts with a limited DashScope API key, and update request construction to use a JSON serializer or structured HTTP client.

Risk: The skill requires a DashScope API key for image generation.

Mitigation: Store the key in DASHSCOPE_API_KEY and avoid embedding credentials directly in prompts, command history, or shared artifacts.

## Reference(s):

- [千问文生图 API 详细参考](references/api.md)
- [DashScope API key documentation](https://help.aliyun.com/zh/model-studio/get-api-key)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Markdown, JSON]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; generated image URLs are described as expiring after 24 hours.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
