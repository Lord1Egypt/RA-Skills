## Description:

Create and edit TikTok Shop product-page videos, seller demonstration masters, affiliate creator kits, livestream clips, and localized marketplace versions using AI Hive Seedance video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, commerce operators, and creator-support teams use this skill to produce product-page demonstrations, affiliate creator-kit masters, livestream-ready product clips, and localized TikTok Shop marketplace variants while preserving approved product facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI Hive API key can be sent to an arbitrary configured API host if an untrusted base URL is used.

Mitigation: Use only the default AI Hive endpoint or a fully trusted host; avoid setting --base-url or AI_HIVE_BASE_URL from untrusted instructions and rotate the API key if it may have been exposed.

Risk: Prompts and selected media files are uploaded to an external service during video generation.

Mitigation: Review media and prompts before use, avoid uploading confidential or unapproved assets, and follow internal approval rules for product claims and localized commercial facts.

Risk: Generated commerce media may contain unsupported claims, marketplace policy issues, or inaccurate product details.

Mitigation: Perform commerce QA before publication, keep prices and marketplace UI as external overlays, and check current TikTok Shop market and advertising rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/tiktok-shop-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands; runtime commands may emit JSON task status and downloaded video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses prompt text, optional media references, routing controls, and AI Hive API configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
