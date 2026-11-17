## Description:

Generates Seedance reference-audio videos through AI Hive by uploading supplied audio or media, submitting a video-generation task, tracking progress, and downloading generated video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, advertising teams, and ecommerce operators use this skill to generate videos from prompts and reference audio for ads, product videos, social content, and short-drama workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation scope is broader than the paid media-upload workflow warrants.

Mitigation: Invoke the skill only when the user explicitly wants Seedance video generation through AI Hive, and confirm media upload and likely costs before submitting a task.

Risk: Prompts and provided media are sent to AI Hive and object storage for generation.

Mitigation: Avoid confidential or sensitive media unless the user has approved that transfer and the AI Hive account terms are acceptable for the content.

Risk: The skill uses a paid local AI Hive API key.

Mitigation: Keep the key out of shared logs and repositories, prefer an isolated environment with pinned dependencies, and rotate the credential if exposure is suspected.

Risk: Repeating generation after a local timeout can submit duplicate paid jobs.

Mitigation: Retain the returned task ID and query task status instead of resubmitting the same generation request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-audio-reference-to-video)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive account and API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, files]

**Output Format:** [CLI text and JSON status output, with generated video files downloaded when enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task IDs for later polling; downloaded media is saved locally, usually as MP4 or MOV depending on the model response.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
