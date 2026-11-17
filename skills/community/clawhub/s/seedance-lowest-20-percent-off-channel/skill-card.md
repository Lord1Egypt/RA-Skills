## Description:

Helps creators, marketing teams, e-commerce teams, and short-form video producers use AI Hive Seedance video generation to create, submit, track, and download videos from text prompts and reference media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, advertising and marketing teams, e-commerce operators, and short-drama producers use this skill to generate or edit Seedance videos through AI Hive. It supports text-to-video, image-to-video, reference-to-video, video editing, video extension, media upload, task tracking, and result download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys, prompts, task IDs, and selected media to the configured AI Hive API service.

Mitigation: Use only when AI Hive Seedance generation is intended, protect the AI_HIVE_API_KEY value, and avoid sharing sensitive prompts or media unless the destination service is approved.

Risk: The skill supports a configurable API base URL, which could direct authenticated requests to an untrusted endpoint.

Mitigation: Keep the default AI Hive API endpoint unless the alternate endpoint is explicitly trusted and reviewed.

Risk: Security evidence marks the release as suspicious because activation text is broad and promotional.

Mitigation: Review the skill before installing or enabling it broadly, and invoke it only for intentional AI Hive Seedance video-generation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-lowest-20-percent-off-channel)
- [ClawHub publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive chat and API key page](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task responses, configuration examples, and downloaded video files from the external generation service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-selected media, submit API-key-authenticated generation tasks, print task IDs and progress, and save completed videos to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
