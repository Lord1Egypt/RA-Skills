## Description:

Create and edit TikTok Shop product listing images, shoppable-video covers, affiliate creator packs and livestream product visuals with reference-guided AI Hive image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and creator teams use this skill to prepare accurate TikTok Shop listing images, shoppable-video covers, affiliate asset packs, livestream cards, ad-test visuals, and localized lifestyle images while preserving merchant-provided product facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference product media and product details may be uploaded to AI Hive during generation.

Mitigation: Use only product or reference files approved for upload to AI Hive, and avoid sending confidential assets unless that service use is permitted.

Risk: The init flow stores an AI Hive API key in a local configuration file.

Mitigation: Use a virtual environment where practical, keep the configuration file private, and rotate the key if the workspace or machine is shared.

Risk: Generated ecommerce images can accidentally include unsupported claims, offers, ratings, certifications, or platform badges.

Mitigation: Review generated images against merchant source facts and current TikTok Shop rules for the target market before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/tiktok-shop-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-selected reference media to AI Hive and download generated image outputs to a configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
