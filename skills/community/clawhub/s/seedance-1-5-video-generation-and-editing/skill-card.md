## Description:

Seedance1.5 视频生成与编辑 helps creators generate and edit videos from text and optional image, video, or audio references through AI Hive, with task submission, progress checks, and finished-video download support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, and advertising or e-commerce teams use this skill to create and revise AI-generated videos for ads, product showcases, social content, short dramas, and related campaign assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local images, videos, or audio to AI Hive for generation or editing.

Mitigation: Confirm that each uploaded file is intended for remote processing and does not contain sensitive, restricted, or unlicensed content.

Risk: Generation tasks may consume paid quota and repeated submissions can create avoidable cost.

Mitigation: Confirm user intent before submitting tasks, preserve returned task IDs, and query existing tasks instead of resubmitting after local timeouts.

Risk: API keys could be exposed if used with an untrusted endpoint or stored insecurely.

Mitigation: Use only trusted AI Hive base URLs, avoid untrusted AI_HIVE_BASE_URL or --base-url values, store credentials carefully, and rotate keys after suspected exposure.

Risk: Broad activation language may cause the skill to appear for adjacent video-tool comparison or migration requests.

Mitigation: Review the user's intent before execution and use the skill only when AI Hive Seedance video generation or editing is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-1-5-video-generation-and-editing)
- [AI Hive API access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit remote video generation tasks, return task identifiers, and download generated video files when executed with valid AI Hive credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
