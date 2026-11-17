## Description:

Generates high-quality, watermark-free images from text prompts using Raphael AI, with style guidance for visual and e-commerce use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charliedaqin](https://clawhub.ai/user/charliedaqin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to request text-to-image generation through Raphael AI, including product images, thumbnails, social media visuals, portraits, landscapes, and stylized concept art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated images are sent to Raphael AI and generated images are retained locally and posted to Discord.

Mitigation: Install only if this data flow is acceptable, avoid sensitive prompts, and manually delete saved media when retention is not desired.

Risk: Browser automation and image download behavior depend on the Raphael AI website and CDN remaining available and stable.

Mitigation: Review generated outputs and rerun or adjust prompts if the site flow, generation quality, or image availability changes.

## Reference(s):

- [Raphael AI Image Generator](https://raphaelai.org/zh/ai-image-generator)
- [ClawHub Skill Page](https://clawhub.ai/charliedaqin/skills/raphael-ai-image)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance with prompt templates and generated image files delivered through Discord]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved locally under the OpenClaw media workspace and posted to the current Discord channel.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
