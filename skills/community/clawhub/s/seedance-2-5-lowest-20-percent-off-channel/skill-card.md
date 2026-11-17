## Description:

This skill helps creators, marketing teams, ecommerce teams, and short-form video teams use AI Hive to generate or edit Seedance 2.5 videos from text and optional image, video, or audio reference media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketers, ecommerce operators, and developers use this skill to prepare AI Hive video-generation or video-editing jobs, upload reference media, poll task status, and download generated videos for ads, product demos, social content, short drama, and comic-style workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference media are sent to AI Hive for processing.

Mitigation: Use the skill only for media and prompts appropriate to send to AI Hive, and avoid sensitive or regulated content unless that service is approved for the intended data.

Risk: The workflow can submit billable video-generation jobs and repeated submissions may incur additional cost.

Mitigation: Review runtime pricing before submission, use low-balance or scoped credentials where available, and query existing task IDs instead of resubmitting after a local timeout.

Risk: Credential and custom endpoint handling require user review before installation.

Mitigation: Store API keys in a protected configuration or environment variable, avoid custom base URLs unless controlled by the user, and rotate credentials if exposure is suspected.

Risk: Downloaded outputs may be written to user-selected directories while filename sanitization is unresolved.

Mitigation: Use a dedicated output directory that does not contain sensitive files, then inspect generated filenames and content before moving outputs elsewhere.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/seedance-2-5-lowest-20-percent-off-channel)
- [AI Hive API Base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API Key Page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, task identifiers, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can upload user-selected media to AI Hive, submit billable generation jobs, poll task status, and download generated MP4, MOV, or runtime-supported video outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
