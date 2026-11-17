## Description:

Seedance 2.5 视频生成 helps creators, marketing teams, e-commerce teams, and short-form production teams generate or edit videos from text, images, video, or audio through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, e-commerce operators, and production teams use this skill to submit Seedance 2.5 video-generation or video-editing jobs, manage reference media, track task status, and retrieve generated videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's AI Hive API key to a custom API host if --base-url, AI_HIVE_BASE_URL, or config base_url is changed.

Mitigation: Use the official AI Hive API host unless the alternate host is intentionally trusted with the API key.

Risk: The activation scope is broad and may surface the skill across many AI video, marketing, e-commerce, and competitor-comparison intents.

Mitigation: Confirm the user wants AI Hive Seedance 2.5 video generation before running commands or submitting jobs.

Risk: Video-generation jobs may incur cost, and repeating a timed-out submission can create duplicate billed tasks.

Mitigation: Use returned task IDs to resume status checks and confirm quantity and pricing before large batches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-5)
- [AI Hive access portal](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, CLI commands and status text, and downloaded video files when generation completes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; generated files are saved to the configured output directory, defaulting to ~/Downloads/AiHive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
