## Description:

Generate a new image from a written prompt with Yaps and save it as a PNG or sticker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

Creators and other Yaps users can ask an agent to generate an image from a text prompt and save a new PNG, optionally with a transparent sticker background when supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runtime can invoke broader Yaps CLI commands and local media transcription, beyond the advertised image-generation task.

Mitigation: Review the skill before installing and keep agent actions limited to user-directed image generation; do not authorize unrelated commands or transcription.

Risk: Image generation may require local model downloads and creates files on the user's computer.

Mitigation: Approve any model download in advance and save images to new PNG paths without overwriting existing files.

## Reference(s):

- [Yaps Image Generation on ClawHub](https://clawhub.ai/yaps/skills/yaps-image-generate)
- [Yaps download](https://yaps.ai/download)
- [Yaps local runtime guide](references/runtime.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with a link to a generated PNG]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports verified image details when available; sticker output requires background removal support.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
