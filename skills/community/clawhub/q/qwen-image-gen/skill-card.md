## Description: <br>
Qwen Image Gen helps an agent generate images with Alibaba Cloud DashScope Qwen-Image models, including synchronous generation, asynchronous task polling, and local PNG downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouweico](https://clawhub.ai/user/zhouweico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create images from prompts, choose Qwen-Image model tiers, run dry-run checks, poll asynchronous image tasks, and save generated PNG files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation settings are sent to Alibaba Cloud DashScope and may create API costs. <br>
Mitigation: Use a scoped or low-risk DASHSCOPE_API_KEY, verify the base URL, start with --dry-run or a single image, and avoid putting secrets or private data in prompts. <br>
Risk: Generated image URLs and task results are time-limited, so delayed retrieval can lose access to outputs. <br>
Mitigation: Download successful results promptly to the configured local output directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouweico/qwen-image-gen) <br>
- [Qwen Image API documentation](https://help.aliyun.com/zh/model-studio/qwen-image-api) <br>
- [Alibaba Model Studio models](https://help.aliyun.com/zh/model-studio/models) <br>
- [API notes](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved as PNG files in the configured output directory; dry-run mode prints request preflight details without calling the API.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
