## Description:

Generates Xiaohongshu-style images from text prompts for home decor, food, fashion, and travel content, using OpenAI DALL-E 3, Stability AI SDXL, or a local image-generation fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, ecommerce sellers, and personal-brand operators use this skill to generate platform-tailored images for Xiaohongshu posts across home decor, food, fashion, and travel themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes unrelated financial API code.

Mitigation: Review the artifact before installation and do not run artifact/scripts/api_client.py unless Tushare financial API access is intentionally needed.

Risk: The supplied dependency file is considered unsafe by the security evidence.

Mitigation: Use a virtual environment and verify external package provenance before installing requirements.txt.

Risk: Cloud generation modes send prompt content to OpenAI or Stability AI.

Mitigation: Treat prompts as data shared with the selected provider and use --use-local when prompt content is sensitive.

Risk: API keys may be exposed during troubleshooting.

Mitigation: Read credentials from environment variables and avoid printing API keys or token values in logs, shell output, or support messages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/skills/xiaohongshu-image-gen)
- [Publisher Profile](https://clawhub.ai/user/utopiabenben)
- [Stability AI SDXL text-to-image endpoint](https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image)
- [Tushare Pro](https://tushare.pro)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration guidance]

**Output Format:** [PNG image files with CLI status text and usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 9:16, 1:1, and 16:9 image aspect ratios; cloud modes send prompts to the selected provider, while local fallback depends on an installed image-generate skill.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
