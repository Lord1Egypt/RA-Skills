## Description:

Create and edit Shopee product listing images, variant galleries, package-content visuals, localized campaign bases, and livestream product cards for Southeast Asian markets using AI Hive generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee sellers, ecommerce creative teams, and marketplace operators use this skill to generate product listing, gallery, livestream, localization, and campaign image bases while preserving SKU, package, variant, and marketplace facts.

### Deployment Geography for Use:

Indonesia, Thailand, Vietnam, Malaysia, the Philippines, Singapore, and Taiwan

## Known Risks and Mitigations:

Risk: The AI Hive API key can be routed to an untrusted custom endpoint if the base URL is overridden.

Mitigation: Keep the base URL set to the official AI Hive endpoint, avoid untrusted --base-url or AI_HIVE_BASE_URL overrides, and protect ~/.ai-hive/config.json.

Risk: Generated ecommerce visuals may include incorrect offers, UI badges, prices, ratings, warranty claims, or localized text if prompts are not reviewed.

Mitigation: Keep offer and platform UI elements outside generated images, validate one marketplace before scaling, and use native reviewers for local copy, units, and current Shopee rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/shopee-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with bash commands; AI Hive task JSON or downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reference images, batch generation, routing mode, model parameters, output directory selection, and submit-only mode.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
