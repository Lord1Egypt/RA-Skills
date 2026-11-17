## Description:

Turns Seedance AI video direction requests into reviewable production plans, shot lists, camera-language prompts, runnable AI-HIVE commands, generation task records, and delivery checklists for commercial, ecommerce, advertising, marketing, short-drama, and social-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Advertising creative teams, directors, producers, brand marketers, and agent operators use this skill to convert scripts, brand goals, authorized product or talent assets, scene constraints, duration, and budget into a production-ready Seedance video workflow. It supports planning first, then optional AI-HIVE API execution for model configuration checks, media upload, price snapshots, routed generation, task polling, download, and local video inspection or formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are required for AI-HIVE calls and can be stored locally or passed through the environment.

Mitigation: Use a limited or test API key, keep secrets out of prompts, logs, screenshots, and version control, and review the local AI-HIVE config before reuse.

Risk: The skill can upload user media and download generated results from AI-HIVE.

Mitigation: Upload only media the user is authorized to share, avoid sensitive media unless the service is trusted, and confirm model, routing, price snapshot, and generation parameters before submission.

Risk: Generated downloads and ffmpeg edits write to local paths and can overwrite files when output paths collide.

Mitigation: Use a dedicated output directory, preserve original source files, inspect target paths before running commands, and avoid reusing filenames for important assets.

Risk: Marketing or product videos can become misleading if the workflow invents product claims, testimonials, platform outcomes, or business facts.

Mitigation: Require sourced facts for product, price, availability, scale, funding, and performance claims, and keep unsupported claims out of scripts and prompts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/seedance-video-director-ai-hive)
- [AI-HIVE chat and API entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands, JSON task records, generated blueprint files, downloaded media files, and ffmpeg-derived video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit billable AI-HIVE generation jobs, upload user-supplied media, poll asynchronous tasks, and write outputs to user-selected local paths.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
