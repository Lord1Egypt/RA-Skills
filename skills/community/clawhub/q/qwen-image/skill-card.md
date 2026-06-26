## Description: <br>
Generate images using Qwen Image API (Alibaba Cloud DashScope). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robin797860](https://clawhub.ai/user/Robin797860) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to generate AI images from Chinese or English text prompts through Alibaba Cloud DashScope and receive either a rendered image URL or, when explicitly requested, a saved image file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation settings are sent to Alibaba Cloud DashScope. <br>
Mitigation: Do not include secrets, regulated data, or sensitive personal data in prompts. <br>
Risk: Passing API keys directly on the command line may expose them in shell history or process listings. <br>
Mitigation: Use a dedicated DashScope API key and prefer environment or agent configuration storage over command-line arguments. <br>
Risk: Disabling SSL verification weakens transport security. <br>
Mitigation: Use --no-verify-ssl only in a controlled proxy setup. <br>
Risk: Generated images can be downloaded to unintended file paths when a filename is provided. <br>
Mitigation: Save files only to paths intentionally chosen by the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Robin797860/qwen-image) <br>
- [Alibaba Cloud DashScope](https://dashscope.aliyuncs.com/) <br>
- [DashScope API key console](https://dashscope.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown image output with command-line text and optional local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns temporary Alibaba Cloud OSS image URLs by default; saves files only when a filename is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
