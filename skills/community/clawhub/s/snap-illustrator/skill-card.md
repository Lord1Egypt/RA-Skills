## Description:

Instantly analyze markdown articles, generate prompts, and seamlessly insert AI illustrations with zero configuration required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wysaid](https://clawhub.ai/user/wysaid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and documentation maintainers use this skill to plan article illustrations, generate image prompts, create images through third-party image services, and insert Markdown image links into long-form content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown content and generated prompts may be sent to third-party image services.

Mitigation: Use the skill only with Markdown content that is appropriate to share with the configured image provider.

Risk: The artifact can use stored Hugging Face credentials without clear current-session consent.

Mitigation: Prefer a session-scoped HF_TOKEN and require explicit user confirmation before using stored provider credentials.

Risk: Proxy settings may be persisted in the skill file.

Mitigation: Avoid storing proxy settings in SKILL.md; pass proxy values through the current command environment when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wysaid/skills/snap-illustrator)
- [Hugging Face Inference Endpoint](https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0)
- [Pollinations Image Endpoint](https://image.pollinations.ai/prompt/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated image files referenced by Markdown image syntax]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; may use HF_TOKEN for Hugging Face fallback image generation.]

## Skill Version(s):

1.0.5 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
