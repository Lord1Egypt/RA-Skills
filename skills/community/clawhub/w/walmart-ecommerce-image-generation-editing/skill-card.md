## Description:

Create and edit Walmart Marketplace product images, variant galleries, package-content views, dimension bases and omnichannel retail visuals using AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers, retail creative operators, and agents use this skill to generate or revise Walmart listing visuals, package-content images, dimension bases, variant galleries, and lifestyle images while preserving catalog facts and avoiding unsupported retail claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured base URL can send API credentials and uploaded product media to an untrusted API origin.

Mitigation: Use only a trusted AI Hive endpoint, and avoid --base-url or AI_HIVE_BASE_URL unless the destination is controlled and approved.

Risk: Reference product images may include proprietary or pre-release assets.

Mitigation: Do not upload sensitive product media without approval; use scoped or throwaway API keys and a pinned virtual environment.

Risk: Generated retail visuals may imply unsupported prices, quantities, certifications, claims, or availability.

Mitigation: Review outputs against the item record and current Walmart Marketplace/category image requirements before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/walmart-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials and may upload reference product media to the configured API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
