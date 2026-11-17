## Description:

Generates page-by-page AI Hive Nano Banana Pro prompts and image jobs for narrative social media marketing carousel campaigns while locking audience, product facts, color, camera, and cross-page rhythm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External social media managers, ecommerce sellers, and brand teams use this skill to plan and generate image-by-image carousel campaigns for platforms such as Instagram, Xiaohongshu, Douyin, WeChat, LinkedIn, Pinterest, and TikTok Shop. It helps keep each page's role, evidence, product facts, visual continuity, and final call to action aligned across a campaign.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected marketing images, prompts, and task metadata are sent to AI Hive for generation.

Mitigation: Use the skill only with images and campaign details that are approved for sharing with AI Hive.

Risk: API keys may be exposed if typed directly in shell history or stored with broad file permissions.

Mitigation: Prefer an environment variable or secure secret manager; if using the skill's auth command, keep the generated config file restricted to the current user.

Risk: Generated visuals or text may contain unsupported claims, inaccurate product details, or platform disclosure issues.

Mitigation: Use the skill's claim-source fields and exclusions, then manually review product facts, claims, text, prices, legal language, and platform safety areas before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/social-media-marketing-image-set-generation)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; the CLI emits generated prompts, task status JSON, and downloaded PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill calls a fixed AI Hive image model, uploads only source images named by the user, polls generation tasks, and saves generated carousel page images to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
