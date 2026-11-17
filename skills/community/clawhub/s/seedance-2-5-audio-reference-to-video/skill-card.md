## Description:

Generates Seedance 2.5 reference-audio videos through AI Hive from a prompt and audio reference, then supports task tracking and result download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, advertisers, and ecommerce teams use this skill to create audio-reference video assets for ads, product showcases, TVC, short drama, social commerce, and social media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be sent to a configured API server.

Mitigation: Use only the default AI Hive endpoint or another endpoint you control and trust; avoid overriding --base-url or AI_HIVE_BASE_URL unless the endpoint is trusted.

Risk: Local media paths supplied for generation are uploaded to AI Hive.

Mitigation: Upload only media that is approved for the target service and does not contain sensitive or restricted content.

Risk: Generated downloads are written to a local output directory.

Mitigation: Use a dedicated output directory and review downloaded files before reuse or publication.

Risk: Long-running or repeated generation tasks may incur cost.

Mitigation: Use no-download mode or task checks for long jobs, retain task IDs, and confirm quantity and live pricing before batch generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-5-audio-reference-to-video)
- [AI Hive chat and API key portal](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; execution can produce JSON task status and generated MP4, MOV, or model-supported video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key. Local media referenced by the user may be uploaded to AI Hive, and generated results are saved to the configured output directory unless no-download mode is used.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
