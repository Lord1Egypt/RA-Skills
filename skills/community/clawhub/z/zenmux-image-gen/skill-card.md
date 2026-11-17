## Description:

Generate images from text prompts using the ZenMux API with Gemini image models, including aspect ratio and resolution controls and optional image-to-image editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkthinking](https://clawhub.ai/user/thinkthinking)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate or edit images from prompts through ZenMux-hosted Gemini image models, saving returned images as local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional input images are sent to ZenMux.

Mitigation: Use the skill only when ZenMux data handling terms are acceptable, and avoid confidential prompts or images unless approved.

Risk: API keys can be exposed if passed on the command line or committed to source control.

Mitigation: Set ZENMUX_API_KEY in the environment and do not use command-line API key arguments or store keys in repository files.

Risk: Generated images may not match the intended prompt or may fail to return image data.

Mitigation: Review generated outputs before use and adjust prompt, model, aspect ratio, or image size when needed.

## Reference(s):

- [ZenMux](https://zenmux.ai)
- [ClawHub skill page](https://clawhub.ai/thinkthinking/skills/zenmux-image-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python script usage; generated images are saved as local files by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script accepts prompt, output path, model, optional input image, temperature, max tokens, aspect ratio, and image size.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
