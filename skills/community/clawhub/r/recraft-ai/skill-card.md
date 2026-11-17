## Description:

Generate, vectorize, upscale, replace background, variate, remove background, and transform images via Recraft API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nkrcrft](https://clawhub.ai/user/nkrcrft)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to call the Recraft API for image generation, image editing, background operations, vectorization, upscaling, and image variations from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to Recraft's external API.

Mitigation: Submit only content appropriate for Recraft's terms and data handling practices.

Risk: API credentials may be exposed if passed on the command line.

Mitigation: Use RECRAFT_API_TOKEN or OpenClaw secret configuration instead of the --api-token argument.

Risk: The user-info command prints account email and credit data when explicitly run.

Mitigation: Run user-info only when that account information is needed and avoid sharing its output in public logs.

## Reference(s):

- [Recraft AI](https://www.recraft.ai/)
- [Recraft API Profile](https://www.recraft.ai/profile/api)
- [ClawHub Skill Page](https://clawhub.ai/nkrcrft/skills/recraft-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and saved image or SVG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script emits saved output paths and MEDIA lines for generated or transformed assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
