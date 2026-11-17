## Description:

MiniMax Image Generation helps agents generate images from text prompts or reference images with MiniMax image-01 and image-01-live, then save generated images locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbos7](https://clawhub.ai/user/turbos7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide an agent through MiniMax text-to-image and image-to-image generation workflows, including model, style, aspect-ratio, batch-size, and local-save options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference images may be sent to MiniMax for generation.

Mitigation: Use the skill only when that third-party data flow is acceptable, and avoid sensitive personal images unless upload is approved.

Risk: Passing an API key with the command-line --api-key option can expose the secret through shell history or process listings.

Mitigation: Prefer MINIMAX_API_KEY or a managed secret store for MiniMax credentials.

## Reference(s):

- [MiniMax Image API Reference](references/image-api.md)
- [MiniMax API Key Console](https://platform.minimaxi.com/user-center/basic-information/interface-key)
- [MiniMax Image Generation API Endpoint](https://api.minimaxi.com/v1/image_generation)
- [ClawHub Skill Page](https://clawhub.ai/turbos7/skills/turbos7-minimax-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples plus local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under ~/.openclaw/workspace/assets/images by default.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
