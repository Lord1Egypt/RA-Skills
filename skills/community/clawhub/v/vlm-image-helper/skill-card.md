## Description:

VLM Image Helper helps agents create clearer intermediate images for VLM and OCR re-analysis by rotating, cropping, zooming, enhancing readability, or converting images for re-input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testlbin](https://clawhub.ai/user/testlbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to improve images for VLM/OCR second-pass analysis when text, small details, or image regions are unclear. It is intended for targeted preprocessing, not general image editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads local images or inline base64 passed to it and can write processed copies or base64 output that may contain sensitive visual content.

Mitigation: Run it only on images you intend to process, choose output paths carefully, and handle generated files or base64 as sensitive when the source image is sensitive.

Risk: Large images or aggressive scale factors can consume substantial local compute or disk or memory.

Mitigation: Prefer semantic crops and modest scale presets before using larger factors, especially on high-resolution inputs.

Risk: The script depends on Pillow for image parsing and transformation.

Mitigation: Install Pillow from trusted or pinned package sources, preferably in a virtual environment.

## Reference(s):

- [CLI Reference](artifact/references/cli-reference.md)
- [Preset Reference](artifact/references/presets.md)
- [ClawHub Skill Page](https://clawhub.ai/testlbin/skills/vlm-image-helper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, plus generated image files or base64 strings from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the provided local image and selected preprocessing operations.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
