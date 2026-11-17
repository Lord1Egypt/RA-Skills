## Description:

Qwen Image Edit helps agents generate and edit images with Alibaba Cloud DashScope Qwen Image models, including text-to-image, single- or multi-image editing, style transfer, and Chinese text-heavy commercial graphics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macwx](https://clawhub.ai/user/macwx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent to generate image URLs or save generated and edited PNG files through Alibaba Cloud DashScope Qwen Image models. It is suited for posters, covers, banners, promotional graphics, text-to-image generation, image cleanup, style transfer, and multi-image fusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected local images may be sent to Alibaba Cloud/DashScope.

Mitigation: Use approved prompts and images only, and avoid private or regulated content unless the service terms and retention rules fit the use case.

Risk: The --no-verify-ssl option can disable TLS certificate verification.

Mitigation: Keep SSL verification enabled except in controlled proxy environments with compensating network controls.

Risk: Providing API keys on the command line can expose credentials through shell history or process listings.

Mitigation: Prefer the DASHSCOPE_API_KEY environment variable and rotate any key that may have been exposed.

## Reference(s):

- [Alibaba Cloud Qwen Image documentation](https://help.aliyun.com/zh/model-studio/text-to-image)
- [Qwen Image Edit on ClawHub](https://clawhub.ai/macwx/skills/qwen-image-edit)
- [Publisher profile](https://clawhub.ai/user/macwx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Markdown image links, MEDIA_URL text lines, and optional PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs expire in 24 hours; local image inputs are base64 encoded before API upload.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
