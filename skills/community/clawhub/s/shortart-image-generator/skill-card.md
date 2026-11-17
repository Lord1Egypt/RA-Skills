## Description:

Generate images with ShortArt AI using text-to-image, image-to-image, e-commerce product image, and template-based workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yige666s](https://clawhub.ai/user/yige666s)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to create ShortArt-generated visual assets from prompts, reference images, e-commerce product inputs, or ShortArt templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated-image download requests may send the ShortArt bearer token to unvalidated image URLs.

Mitigation: Avoid the download workflow until image URL hosts are validated and the Authorization header is only sent to trusted ShortArt endpoints.

Risk: Prompts and uploaded images are sent to the ShortArt service.

Mitigation: Use only non-sensitive prompts and images that are acceptable to share with ShortArt.

Risk: The release has unavailable server-resolved source provenance.

Mitigation: Prefer a pinned, verified install source and review the artifact before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yige666s/skills/shortart-image-generator)
- [ShortArt Home](https://shortart.ai)
- [ShortArt API Key Setup](https://shortart.ai/key)
- [Text-to-Image Generation](references/text-to-image.md)
- [E-commerce Suit Image Generation](references/suit-image.md)
- [Template-based Image Generation](references/template-image.md)
- [Image Prompt Writing Guide](references/prompt-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return ShortArt project IDs, polling status, generated image metadata, and local download paths.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
