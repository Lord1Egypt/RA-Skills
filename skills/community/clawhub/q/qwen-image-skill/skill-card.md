## Description: <br>
Generates images with Alibaba Cloud Bailian Qwen-Image and Z-Image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irron](https://clawhub.ai/user/irron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate local image files from text prompts through DashScope, with automatic model selection for portrait, photo, and general image-generation scenarios. <br>

### Deployment Geography for Use: <br>
Global, subject to Alibaba Cloud DashScope regional API-key availability. <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Alibaba Cloud for generation. <br>
Mitigation: Avoid sensitive or confidential prompt content and review the provider terms before use. <br>
Risk: The skill requires a DashScope API key. <br>
Mitigation: Use a dedicated, revocable key via DASHSCOPE_API_KEY and do not commit secrets in TOOLS.md. <br>
Risk: An explicit output path can overwrite an existing local file. <br>
Mitigation: Choose output paths carefully and write generated images to a controlled directory. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen-Image API documentation](https://help.aliyun.com/zh/model-studio/qwen-image-api) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/) <br>
- [ClawHub release page](https://clawhub.ai/irron/qwen-image-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Image files, Shell commands, Configuration guidance] <br>
**Output Format:** [PNG image files plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; accepts prompt, model, size, watermark, prompt extension, and output path options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
