## Description: <br>
Generates high-quality images with Volcengine Seedream-4.5 from text prompts, reference images, or sequential grouped-image requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crabfishxy](https://clawhub.ai/user/crabfishxy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and image creators use this skill to ask an agent to call Volcengine Seedream for text-to-image, image-to-image, and grouped image generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to Volcengine for generation. <br>
Mitigation: Use the skill only with content that is acceptable to share with Volcengine and avoid sensitive prompts or private reference images. <br>
Risk: The Volcengine API key may consume account quota or incur costs. <br>
Mitigation: Use a dedicated limited-use key where possible and monitor account usage. <br>
Risk: Passing an API key on the command line can expose it in shared shell history. <br>
Mitigation: Prefer the VOLC_API_KEY environment variable instead of pasting secrets into command arguments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/crabfishxy/seedream-image-for-openclaw) <br>
- [Volcengine Seedream image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Plain text MEDIA_URL lines with Markdown image embeds for display] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return one or more image URLs; sequential mode supports up to 15 images.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
