## Description: <br>
Visual Muse helps an agent turn natural-language image requests into ComfyUI image-generation workflows with prompt creation, model selection, batch generation, quality review, and preference memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baobaodawang-creater](https://clawhub.ai/user/baobaodawang-creater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images through a local ComfyUI setup from natural-language prompts, with support for style templates, workflow preparation, model fallback, quality review, and local preference tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bundles setup and administration scripts for a local ComfyUI stack. <br>
Mitigation: Review the shell scripts before running them and install only in an environment where local ComfyUI administration is acceptable. <br>
Risk: ComfyUI may be exposed on all network interfaces if launched with broad listen settings. <br>
Mitigation: Bind ComfyUI only to intended interfaces unless remote access is required and protected. <br>
Risk: Troubleshooting cleanup commands can remove local session or workspace data. <br>
Mitigation: Create and verify backups before running cleanup commands or deleting session directories. <br>
Risk: Prompts, preferences, run history, and Ofox-routed LLM requests may leave local-only control boundaries. <br>
Mitigation: Avoid sensitive prompts, review provider data handling, and disable model switching paths that are not needed. <br>


## Reference(s): <br>
- [Visual Muse on ClawHub](https://clawhub.ai/baobaodawang-creater/visual-muse) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI.git) <br>
- [ComfyUI Desktop](https://www.comfy.org/download) <br>
- [Stable Diffusion XL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) <br>
- [DreamShaper XL](https://huggingface.co/Lykon/DreamShaper) <br>
- [Juggernaut XL v9](https://huggingface.co/RunDiffusion/Juggernaut-XL-v9) <br>
- [Animagine XL 3.1](https://huggingface.co/cagliostrolab/animagine-xl-3.1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown or text responses with JSON payloads, shell commands, configuration edits, and generated image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are produced through a local ComfyUI service and written to local output directories when the required ComfyUI environment is available.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
