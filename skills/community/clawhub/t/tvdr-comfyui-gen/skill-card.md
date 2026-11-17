## Description:

Provides ComfyUI-based image generation with workflow validation, prompt-field checks, retry handling, and output-file handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admirobot](https://clawhub.ai/user/admirobot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-creation agents use this skill to submit prompts and validated ComfyUI workflows to a configured ComfyUI server, then retrieve generated image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and full workflow JSON are sent to a configurable plain-HTTP ComfyUI server.

Mitigation: Use a loopback or authenticated HTTPS endpoint, and avoid sending sensitive prompts or workflow content.

Risk: Generated or downloaded content can be written to caller-chosen output paths.

Mitigation: Restrict output paths to a dedicated directory where overwrites are acceptable.

Risk: Unreviewed workflow templates can change generation behavior or route data unexpectedly.

Mitigation: Use reviewed workflow templates and keep workflow validation enabled before submitting generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/admirobot/skills/tvdr-comfyui-gen)
- [Publisher profile](https://clawhub.ai/user/admirobot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python API return dictionaries and Markdown usage examples with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, file path, file size, prompt ID, duration, and error details when generation fails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
