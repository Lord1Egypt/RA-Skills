## Description: <br>
Generate images and videos via Runware API. Access to FLUX, Stable Diffusion, Kling AI, and other top models. Supports text-to-image, image-to-image, upscaling, text-to-video, and image-to-video. Use when generating images, creating videos from prompts or images, upscaling images, or doing AI image transformation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[26medias](https://clawhub.ai/user/26medias) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate, transform, upscale, and animate images and videos through Runware models from agent-generated shell commands and configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Runware for generation, transformation, upscaling, or video creation. <br>
Mitigation: Avoid sensitive or regulated content unless Runware's terms and data handling meet the user's requirements. <br>
Risk: Runware API calls may consume paid credits. <br>
Mitigation: Review model choice, dimensions, count, duration, and pricing before running generation commands. <br>
Risk: Passing the API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer the RUNWARE_API_KEY environment variable over command-line API key arguments. <br>


## Reference(s): <br>
- [Runware](https://runware.ai) <br>
- [Runware Models](https://runware.ai/models) <br>
- [Runware Pricing](https://runware.ai/pricing) <br>
- [Runware API Endpoint](https://api.runware.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated media file paths from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded image or video files when the helper scripts are executed with a Runware API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
