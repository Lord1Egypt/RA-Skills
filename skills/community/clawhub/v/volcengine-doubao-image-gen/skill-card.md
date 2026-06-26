## Description: <br>
Generates images and short videos through Volcengine Doubao APIs, including Seedream image workflows and Seedance video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goodgooddayhi](https://clawhub.ai/user/goodgooddayhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate Doubao images, image variations from reference URLs, multi-image sequences, and short Seedance videos from prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The video workflow reads /root/.openclaw/workspace/.env, which can expose unrelated environment secrets to the runtime context. <br>
Mitigation: Use a dedicated ARK_API_KEY and avoid storing unrelated secrets in that shared .env file. <br>
Risk: The scripts write generated media to user-supplied output paths. <br>
Mitigation: Use simple relative filenames in a dedicated output directory and review files before sharing or overwriting existing assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goodgooddayhi/volcengine-doubao-image-gen) <br>
- [Volcengine Ark console](https://console.volcengine.com/ark) <br>
- [Volcengine image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and may write generated image or video files to user-selected output paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
