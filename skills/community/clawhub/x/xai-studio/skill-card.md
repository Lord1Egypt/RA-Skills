## Description:

xAI Studio generates and edits images and videos through the xAI API, covering image generation, image editing, style transfer, multi-turn chaining, text-to-video, image-to-video, and video editing from a CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h0llyw00dzz](https://clawhub.ai/user/h0llyw00dzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate, edit, and batch-process images and videos from prompts or source media through xAI models. It is suitable when an agent needs CLI-backed media workflows with generated outputs saved locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected image or video inputs are sent to xAI for processing.

Mitigation: Use only prompts and media that are acceptable to share with xAI, and avoid sensitive content unless that use is explicitly approved.

Risk: The xai-sdk dependency may change behavior across releases if installed without version control.

Mitigation: Pin xai-sdk in a controlled virtual environment and review dependency updates before rollout.

Risk: Generated media is saved to a local output directory and may persist after the command finishes.

Mitigation: Choose an appropriate output directory and apply local retention, access control, or cleanup practices for generated files.

## Reference(s):

- [xAI Studio ClawHub page](https://clawhub.ai/h0llyw00dzz/skills/xai-studio)
- [xAI Studio homepage](https://github.com/H0llyW00dzZ/xai-studio-skills)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration]

**Output Format:** [CLI output plus generated image or video files saved under the configured output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY and xai-sdk; image outputs may be PNG, JPEG, WebP, or GIF, and video outputs are MP4.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
