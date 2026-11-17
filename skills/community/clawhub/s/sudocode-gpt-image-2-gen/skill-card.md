## Description:

This skill helps agents generate, edit, and combine images through SudoCode's GPT Image 2 image API with size, quality, format, and reference-image controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengy983](https://clawhub.ai/user/shengy983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to create new images, edit existing images, or fuse multiple reference images by invoking the bundled Node.js or Python helpers against the SudoCode GPT Image 2 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled prompts, filenames, or image paths could create command-injection exposure if interpolated into shell command templates.

Mitigation: Invoke the helper scripts with structured argument arrays or fully escape user-controlled values before execution.

Risk: API keys may be exposed through command history or process listings if passed as command-line flags.

Mitigation: Prefer environment variables for secrets and avoid pasting API keys into command-line flags on shared systems.

Risk: Prompts and uploaded reference images are sent to the configured SudoCode-compatible API endpoint.

Mitigation: Use the skill only with data approved for that external service and confirm the configured API endpoint before sending sensitive content.

## Reference(s):

- [SudoCode platform](https://sudocode.us)
- [ClawHub skill page](https://clawhub.ai/shengy983/skills/sudocode-gpt-image-2-gen)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a SudoCode-compatible external API, upload reference images for edits, and write PNG, JPEG, or WebP files to disk.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
