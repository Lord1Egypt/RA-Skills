## Description:

Uses Nano Banana Pro to migrate Stable Diffusion, SDXL, WebUI, ComfyUI, checkpoint, LoRA, ControlNet, and negative-prompt workflows into AI Hive reference images and natural-language constraints without running or distributing third-party model weights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and external AI image workflow users use this skill to translate Stable Diffusion-style prompts, reference images, LoRA/ControlNet intent, denoise instructions, and negative prompts into AI Hive image-generation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected reference images, and the AI Hive API key are sent to AI Hive.

Mitigation: Use the skill only with data appropriate for AI Hive processing, avoid highly sensitive images, and provide API keys through the supported environment, CLI, or local config paths.

Risk: The dependency is installed as an unpinned requests package in the usage notes.

Mitigation: Use a pinned requirements file or controlled Python environment before deployment.

Risk: Downloaded result URLs and file sizes are not tightly constrained.

Mitigation: Monitor output downloads and run the tool in a workspace with appropriate storage limits.

Risk: Stable Diffusion seed and node settings do not map pixel-for-pixel to the AI Hive model.

Mitigation: Review generated images against the intended control intent, subject facts, licensing source, and cross-sample consistency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/stable-diffusion-image-generation-editing-alternative)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; the CLI can return JSON task details and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; uses the fixed public_model_nano_banana_pro model; accepts optional reference images and key=value model parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
