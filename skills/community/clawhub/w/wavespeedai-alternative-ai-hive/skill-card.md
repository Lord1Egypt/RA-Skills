## Description:

Helps AIGC, ecommerce, and advertising teams evaluate AI-HIVE as a WaveSpeedAI alternative and produce migration audits, compatibility checks, routing plans, runnable examples, task ledgers, and acceptance criteria for image, video, reference-asset, and asynchronous generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content operations teams, and AI integration engineers use this skill to plan and test a controlled migration or fallback route from WaveSpeedAI to AI-HIVE for image, video, ecommerce, advertising, marketing, short-drama, comic-video, and batch generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run paid AI-HIVE generation workflows that consume account credits.

Mitigation: Start with small authorized test jobs, confirm routing, model choice, budget, and pricing snapshots before running batch generation, and keep production cutover gated by measured acceptance criteria.

Risk: Selected local media may be uploaded to AI-HIVE or object storage and generated files may be downloaded locally.

Mitigation: Use only authorized media, avoid sensitive or third-party restricted assets unless permitted, and review local output paths before sharing or committing files.

Risk: API key handling is sensitive and the security evidence recommends avoiding persisted credentials.

Mitigation: Provide the AI-HIVE API key through the AI_HIVE_API_KEY environment variable, keep keys out of files, logs, screenshots, archives, and version control, and rotate credentials after testing when appropriate.

Risk: Custom API base URLs could redirect requests or credentials to an untrusted service.

Mitigation: Use the default AI-HIVE API endpoint unless the alternate base URL is fully trusted and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/wavespeedai-alternative-ai-hive)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base](https://ai-hive.iclip.cn/api)
- [WaveSpeedAI reference page](https://wavespeed.ai/seedance-2-api)
- [Platform Source and Comparison Boundaries](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with runnable shell commands and generated JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create migration audit, blueprint, image generation, video generation, task ledger, and media processing files when the helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
