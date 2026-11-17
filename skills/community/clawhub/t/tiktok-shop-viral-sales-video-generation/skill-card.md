## Description:

Create and edit TikTok Shop UGC sales videos, product demos, unboxings, Spark Ads and GMV Max creative variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, marketers and agent operators use this skill to prepare TikTok Shop and social-commerce UGC video generation workflows for product demos, unboxings, localized sales videos, Spark Ads variants and GMV Max creative variants. It helps preserve merchant-provided product, offer and compliance facts while producing prompts and commands for AI Hive video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI Hive API keys.

Mitigation: Install only if you trust AI Hive and the publisher, and use a dedicated API key with limited balance or permissions where possible.

Risk: The skill can upload local product photos, videos and audio to AI Hive for generation.

Mitigation: Run it in a constrained environment for sensitive media and upload only merchant-approved assets with appropriate usage rights.

Risk: Changing the base URL can send requests and credentials to a non-official host.

Mitigation: Avoid setting AI_HIVE_BASE_URL or --base-url to non-official hosts.

Risk: Generated files are downloaded to a local output directory.

Mitigation: Choose an output directory where accidental overwrites would not be damaging, or use no-download mode while reviewing task results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/tiktok-shop-viral-sales-video-generation)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, text]

**Output Format:** [Markdown guidance with bash commands, configuration examples and task-status JSON when commands are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated video media can be downloaded to a local output directory by the CLI unless no-download mode is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
