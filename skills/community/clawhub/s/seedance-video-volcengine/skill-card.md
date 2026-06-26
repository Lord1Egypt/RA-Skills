## Description: <br>
Generate AI videos with ByteDance Seedance (Doubao/Volcengine Ark) via Ark API, supporting text-to-video and image-to-video with the doubao-seedance-1-5-pro-251215 model endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maddy-cc](https://clawhub.ai/user/maddy-cc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate videos from text prompts or public image URLs through Volcengine Ark/Seedance. It provides curl-based task creation, polling, video URL retrieval, download guidance, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image URLs are sent to Volcengine Ark/Seedance, which may expose confidential, personal, private, or regulated content to an external provider. <br>
Mitigation: Use a dedicated Ark API key and avoid submitting confidential prompts, private images, personal data, or regulated content unless approved for that provider. <br>
Risk: Video generation can consume provider quota or incur costs. <br>
Mitigation: Review Ark cost, quota, and endpoint settings before running generation tasks. <br>
Risk: Generated video URLs are temporary and can fail if the signed query string is copied incompletely. <br>
Mitigation: Download successful MP4 outputs promptly with the complete signed URL, including all query parameters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maddy-cc/seedance-video-volcengine) <br>
- [Volcengine Ark console](https://console.volcengine.com/ark) <br>
- [Volcengine video generation API documentation](https://www.volcengine.com/docs/82379/1520757) <br>
- [GitHub Issues support](https://github.com/maddy-cc/seedance-video-skill/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks, JSON request examples, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and sends prompts or public image URLs to Volcengine Ark.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
