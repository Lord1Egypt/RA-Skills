## Description: <br>
Generate images with Model Studio DashScope SDK using Qwen Image generation models (qwen-image-max, qwen-image-plus-2026-01-09). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement or document Alibaba Cloud Model Studio DashScope Qwen image generation with normalized image.generate requests and responses for agent pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can read DashScope API keys from environment variables or local Alibaba Cloud credentials. <br>
Mitigation: Install only when DashScope/Qwen image generation is intended and run it in a controlled workspace with appropriate credential access. <br>
Risk: Generated images can be written to local paths. <br>
Mitigation: Use explicit output paths in a workspace you control and review files before reuse or publication. <br>
Risk: Requested results may be sent through Telegram or another channel delivery target. <br>
Mitigation: Enable channel delivery only when the image should be returned to that requester and use an explicit target. <br>
Risk: Reference image paths may expose local sensitive files if passed unintentionally. <br>
Mitigation: Avoid passing sensitive reference-image paths unless they are deliberately intended for generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-alicloud-ai-image) <br>
- [Publisher profile](https://clawhub.ai/user/fresh3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local image files when the helper script is run with a DashScope API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
