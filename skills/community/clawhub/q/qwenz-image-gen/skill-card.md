## Description: <br>
Generate images using Alibaba Cloud Bailian Qwen-Image and Z-Image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irron](https://clawhub.ai/user/irron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate image assets from text prompts with Alibaba Cloud Bailian models, selecting portrait-focused or general image models automatically or by command-line option. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends image prompts to Alibaba Cloud DashScope for generation. <br>
Mitigation: Do not include confidential data or sensitive personal information in prompts. <br>
Risk: The skill requires an Alibaba DashScope API key and can read it from environment configuration or TOOLS.md. <br>
Mitigation: Use an environment variable or a dedicated low-scope key, and avoid committing TOOLS.md with secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/irron/qwenz-image-gen) <br>
- [Alibaba Cloud Model Studio Qwen-Image API](https://help.aliyun.com/zh/model-studio/qwen-image-api) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line status text and a locally saved PNG image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and sends prompts to Alibaba Cloud DashScope for image generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
