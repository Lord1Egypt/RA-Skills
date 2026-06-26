## Description: <br>
Generate images using SiliconFlow API (FLUX.1, Stable Diffusion, etc.) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate images from text prompts through SiliconFlow models and optionally save generated files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and API credentials are used with the SiliconFlow service, which may incur charges and expose prompt content to that provider. <br>
Mitigation: Use a dedicated, revocable SiliconFlow API key and avoid submitting prompts that contain sensitive information. <br>
Risk: Generated images can be saved to local paths selected at run time. <br>
Mitigation: Choose output paths intentionally and review generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lilei0311/siliconflow-image-gen) <br>
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with image URLs and optional local image file paths, plus Markdown usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SiliconFlow API key and may write generated image files to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
