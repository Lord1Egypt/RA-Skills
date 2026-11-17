## Description:

Visual Muse helps OpenClaw agents turn natural-language image requests into ComfyUI prompts, workflows, generated image files, quality reviews, and preference-aware guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baobaodawang-creater](https://clawhub.ai/user/baobaodawang-creater)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative operators use this skill to generate images from natural-language requests through a local ComfyUI setup. The skill also supports prompt preparation, workflow selection, batch generation, result review, troubleshooting, and preference tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or connect to a local ComfyUI service and depends on OpenClaw workspace paths.

Mitigation: Bind ComfyUI to 127.0.0.1 unless remote access is intentionally required, and review workspace path access before installation.

Risk: Setup and troubleshooting flows can download large third-party model artifacts and dependencies.

Mitigation: Use trusted model sources, verify downloaded artifacts where practical, and install only in an environment prepared for the storage and compute requirements.

Risk: Troubleshooting cleanup commands can remove local session or workspace files if copied without review.

Mitigation: Inspect command targets first and make a verified backup before running cleanup commands.

## Reference(s):

- [Visual Muse Skill Page](https://clawhub.ai/baobaodawang-creater/skills/visual-muse)
- [Visual Muse README](artifact/README.md)
- [Visual Muse Troubleshooting](artifact/TROUBLESHOOTING.md)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI.git)
- [SDXL Base 1.0 Model Card](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
- [DreamShaper XL Model Card](https://huggingface.co/Lykon/DreamShaper)
- [Juggernaut XL Model Card](https://huggingface.co/RunDiffusion/Juggernaut-XL-v9)
- [Animagine XL 3.1 Model Card](https://huggingface.co/cagliostrolab/animagine-xl-3.1)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown status messages, JSON prompt and workflow payloads, shell command invocations, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local ComfyUI service, COMFYUI_API_URL configuration, Python tooling, and local model files.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
