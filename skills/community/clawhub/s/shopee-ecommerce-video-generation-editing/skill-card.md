## Description:

Create and edit Shopee product videos, localized demos, short-form ads and seller campaign assets for Southeast Asian markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, marketers, and developers use this skill to create localized, mobile-first Shopee product videos, demos, unboxings, campaign variants, and edits while preserving merchant-approved product facts.

### Deployment Geography for Use:

Indonesia, Thailand, Vietnam, Malaysia, the Philippines, Singapore, Taiwan, and other Shopee seller markets as policy permits

## Known Risks and Mitigations:

Risk: A configurable AI Hive base URL can redirect the API key and selected media to an untrusted host.

Mitigation: Use the default AI Hive endpoint unless a custom deployment is fully trusted, and prevent agents, environment variables, and config files from setting untrusted base URLs.

Risk: The skill stores and uses an AI Hive API key and uploads user-selected media for generation.

Mitigation: Treat the API key in ~/.ai-hive/config.json as sensitive, restrict file permissions, and confirm that uploaded media is appropriate for the target service before generation.

Risk: Generated ecommerce videos can introduce unsupported product, pricing, voucher, rating, warranty, or platform claims.

Mitigation: Review generated outputs against merchant-approved facts, current Shopee seller and advertising rules, and native-language copy review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/shopee-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key and account page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples, configuration JSON, API task status, and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-selected images, videos, or audio to AI Hive and download generated video results unless no-download mode is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
