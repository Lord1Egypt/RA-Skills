## Description:

Generate images using Alibaba Cloud Bailian Qwen-Image and Z-Image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irron](https://clawhub.ai/user/irron)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate images from text prompts through Alibaba Cloud Bailian Qwen-Image and Z-Image models, with automatic model selection for portrait and general image prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read API keys from local TOOLS.md files, including a hardcoded path, before calling Alibaba Cloud.

Mitigation: Set DASHSCOPE_API_KEY explicitly in the session environment and avoid storing organization-managed API keys in shared TOOLS.md files.

Risk: Image-generation prompts are sent to Alibaba Cloud.

Mitigation: Do not submit confidential prompts or sensitive data unless the environment and provider terms are approved for that use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/irron/skills/qwenz-image-gen)
- [Alibaba Cloud Model Studio Qwen-Image API documentation](https://help.aliyun.com/zh/model-studio/qwen-image-api)
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and sends image-generation prompts to Alibaba Cloud.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
