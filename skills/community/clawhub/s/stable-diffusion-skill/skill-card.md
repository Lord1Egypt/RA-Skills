## Description: <br>
Stable Diffusion Skill helps agents generate, edit, upscale, and manage images through a configured Stable Diffusion WebUI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markcookie](https://clawhub.ai/user/markcookie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image creators use this skill to ask an agent to generate images from prompts, transform or inpaint existing images, apply ControlNet or LoRA options, switch SD WebUI models, and upscale outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and supplied images are sent to the configured Stable Diffusion WebUI API. <br>
Mitigation: Keep SD_WEBUI_URL pointed at a trusted local or private server and avoid sending sensitive prompts or images to untrusted endpoints. <br>
Risk: Model-switching and output-directory commands can change the active generation model or write image files locally. <br>
Mitigation: Review model names, paths, and output directories before running generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markcookie/stable-diffusion-skill) <br>
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python command examples and generated image files from SD WebUI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, requests, Pillow, and SD_WEBUI_URL pointed at a trusted Stable Diffusion WebUI API; generated images are saved to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
