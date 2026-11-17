## Description:

Generates and edits Seedance2.5 videos from text prompts and optional image, video, or audio references through AI Hive, with task tracking and result download support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, marketers, and e-commerce teams use this skill to generate, edit, extend, and adapt video assets for ads, product showcases, social commerce, short drama, and social media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI Hive API keys and allows endpoint override through command-line or environment configuration.

Mitigation: Use a dedicated low-limit API key and avoid `--base-url` or `AI_HIVE_BASE_URL` unless the endpoint is fully trusted.

Risk: The skill can upload local images, videos, and audio files to the configured service endpoint.

Mitigation: Review media files before use and upload only files intended for processing by AI Hive.

Risk: Video generation and batch workflows may incur service costs.

Mitigation: Check runtime pricing, use `--no-download` for small validation submissions when appropriate, and confirm cost expectations before batch jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-5-video-generation-and-editing)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON snippets, and downloaded media files from the invoked service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit billable AI Hive video tasks, upload local media references, return task IDs, and download generated MP4, MOV, or service-supported video outputs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
