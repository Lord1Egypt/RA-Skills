## Description:

Generates Seedream 5.0 Lite livestream commerce images for previews, openings, product explanations, promotion cards, transitions, endings, and replay covers through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, and developers use this skill to generate time-boxed livestream shopping images with approved product references, safe UI areas, and placeholders for live price, stock, coupon, and countdown fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if copied into shell history or shared logs.

Mitigation: Use the config file or AI_HIVE_API_KEY environment variable instead of passing the key on the command line, and keep the config file permission-restricted.

Risk: Reference images may contain assets, people, brands, or private content the user is not allowed to send to AI Hive.

Mitigation: Upload only images the user is authorized to process with the service.

Risk: Generated livestream cards may include incorrect or stale pricing, stock, discount, or countdown information if those fields are finalized too early.

Mitigation: Keep live commercial fields as placeholders and require operational review before publishing or airing.

Risk: Generated visuals may misstate product details, brand elements, platform UI constraints, or live-event facts.

Mitigation: Review product identity, logos, claims, safe areas, and approval records before using generated assets in a livestream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-livestream-image)
- [AI Hive API endpoint used by the helper](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline bash commands; generated image files are downloaded by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper submits image-generation tasks, optionally uploads user-provided reference images, polls task status, and downloads completed image results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
