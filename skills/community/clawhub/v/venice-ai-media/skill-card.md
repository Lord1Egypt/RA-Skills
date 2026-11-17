## Description:

Generate, edit, and upscale images and create videos from images via Venice AI, with support for text-to-image, image-to-video (Sora, WAN), upscaling, and AI editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhannah](https://clawhub.ai/user/nhannah)

### License/Terms of Use:


## Use Case:

Developers and creative operators use this skill to generate images, edit and upscale existing images, quote and create image-to-video jobs, and return generated media files from Venice AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL-based image inputs can fetch arbitrary internal, private, or large URLs from the user's machine and forward them to Venice.

Mitigation: Prefer local image files; only pass trusted public image URLs; avoid internal, private, or unusually large URLs.

Risk: The Venice API key may be stored in the user environment or Clawdbot configuration file.

Mitigation: Protect the configuration file, keep API keys out of shared logs and prompts, and rotate keys if exposure is suspected.

Risk: Embedding prompts in image EXIF metadata can disclose sensitive generation details.

Mitigation: Avoid --embed-exif for sensitive prompts or when generated files will be shared externally.

Risk: --no-validate can bypass model availability checks and affect cost, behavior, or safety filtering.

Mitigation: Use model validation by default, run --list-models before selecting new models, and use --quote for video generation cost checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nhannah/skills/venice-ai-media)
- [Venice AI Homepage](https://venice.ai)
- [Venice API Key Settings](https://venice.ai/settings/api)
- [Venice API Base Endpoint](https://api.venice.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, media files]

**Output Format:** [Markdown guidance with shell commands and generated media file paths; scripts print MEDIA lines for attachment.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+ and VENICE_API_KEY; output media can be image or video files depending on the selected command.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
