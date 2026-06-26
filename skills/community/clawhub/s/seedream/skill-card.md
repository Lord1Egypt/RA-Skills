## Description: <br>
Generate and edit AI images with ByteDance Seedream models through Atlas Cloud, including text-to-image, image editing, batch sequential generation, PNG output, prompt optimization, and high-resolution outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to generate, edit, and batch-produce images for posters, product visuals, brand assets, social media graphics, illustrations, and concept art using Seedream models via Atlas Cloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and uploaded local images are sent to Atlas Cloud for generation or editing. <br>
Mitigation: Avoid confidential prompts and sensitive images unless the user accepts Atlas Cloud processing for that content. <br>
Risk: Atlas Cloud usage is paid per generated image and larger batches can increase cost. <br>
Mitigation: Confirm model, output count, and batch settings before running larger generation jobs. <br>
Risk: The Atlas Cloud API key grants access to all models available on the user's account. <br>
Mitigation: Store ATLASCLOUD_API_KEY only in the environment and monitor account usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/seedream) <br>
- [Metadata homepage](https://github.com/AtlasCloudAI/nano-banana-2-skill) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>
- [Seedream 5.0 pricing reference](https://fal.ai/seedream-5.0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated image files saved locally by the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY and sends prompts, image URLs, and uploaded local images to Atlas Cloud when used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
