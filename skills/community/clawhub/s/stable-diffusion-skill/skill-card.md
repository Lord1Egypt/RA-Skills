## Description:

Complete Stable Diffusion WebUI integration skill for image generation, image editing, inpainting, ControlNet, LoRA, model switching, and upscaling through the SD WebUI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markcookie](https://clawhub.ai/user/markcookie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to guide an agent through Stable Diffusion WebUI image generation and editing workflows. It helps prepare prompts, run txt2img and img2img commands, use inpainting and ControlNet, manage models and LoRA references, and upscale generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images can be sent to the configured Stable Diffusion WebUI endpoint.

Mitigation: Keep SD_WEBUI_URL on localhost or a trusted HTTPS endpoint, and avoid sending sensitive images to remote servers.

Risk: Generated galleries or output directories may include untrusted filenames.

Mitigation: Use trusted output directories and inspect filenames before opening generated galleries.

Risk: Generated images may be subject to user, model, copyright, and usage-policy obligations.

Mitigation: Review generated outputs and confirm the applicable Stable Diffusion WebUI and model terms before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markcookie/skills/stable-diffusion-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/markcookie)
- [Stable Diffusion WebUI project homepage](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image files in a local output directory through the configured Stable Diffusion WebUI endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
