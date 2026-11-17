## Description:

Generates new images from a reference image and prompt using Tomoviee's Image-to-Image API through the Wondershare OpenAPI gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative production teams use this skill to create subject-preserving image variations, style transfers, and scene changes from a prompt and reference image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Tomoviee API credentials can be exposed through command-line arguments or printed authorization tokens.

Mitigation: Use environment variables or a secrets manager outside the skill, avoid the token helper for real credentials, and prevent agents from printing Authorization tokens.

Risk: Reference image URLs, prompts, callback URLs, and passthrough params are submitted to Tomoviee/Wondershare endpoints.

Mitigation: Submit only data approved for third-party processing and avoid sensitive images, private URLs, or callbacks that expose internal services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/tomoviee-reference-to-image)
- [Tomoviee Image-to-Image API Docs](https://www.tomoviee.ai/doc/ai-image/image-to-image.html)
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html)
- [Tomoviee Image-to-Image API Docs (Mainland)](https://www.tomoviee.cn/doc/ai-image/image-to-image.html)
- [Image API Reference](references/image_apis.md)
- [Prompt Engineering Guide](references/prompt_guide.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with Python snippets and shell commands; API responses are JSON with task status and generated image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates asynchronous image-generation tasks and polls for completion.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
