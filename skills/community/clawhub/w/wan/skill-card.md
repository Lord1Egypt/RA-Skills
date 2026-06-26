## Description: <br>
Generate images using Alibaba DashScope wan2.6-t2i model, download to Desktop, and upload to catbox.moe image hosting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxyd-ai](https://clawhub.ai/user/lxyd-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to generate images from text prompts through Alibaba DashScope, save the generated image locally, and optionally publish it through catbox.moe for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure from copying or logging a DashScope API key. <br>
Mitigation: Use only a user-provided DashScope key, keep it in an environment variable, and avoid pasting secrets into logs or shared chats. <br>
Risk: Prompts are sent to Alibaba DashScope and generated images may be uploaded to public catbox.moe hosting. <br>
Mitigation: Use the skill only for prompts and images that are acceptable to share with those external services, and confirm before publishing generated files. <br>
Risk: Generated image URLs can expire before download completes. <br>
Mitigation: Download generated images immediately after receiving the DashScope response and regenerate the image if the URL returns an expiration error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxyd-ai/wan) <br>
- [DashScope multimodal generation endpoint](https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation) <br>
- [catbox.moe upload endpoint](https://catbox.moe/user/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and generated image file paths or public image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided DASHSCOPE_API_KEY; generated images are downloaded locally and may be uploaded to public hosting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
