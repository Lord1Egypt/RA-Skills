## Description:

Seedance 视频生成与编辑 helps agents create or edit videos through AI Hive from a text prompt and optional image, video, audio, first-frame, or last-frame references, then track the task and download results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, and advertising or commerce teams use this skill to generate product, ad, social, short-drama, and other marketing videos without writing API code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an AI Hive API key.

Mitigation: Prefer the 0600 configuration file or environment variable over passing the key directly on the command line.

Risk: The skill can upload selected media to AI Hive.

Mitigation: Review media paths before running commands and avoid uploading files that contain sensitive or unapproved content.

Risk: Video-generation requests may spend service credits.

Mitigation: Confirm routing, model pricing, and task volume before running batch or high-cost generation workflows.

Risk: The API base URL can be overridden.

Mitigation: Use the default AI Hive endpoint unless a trusted operator has explicitly approved a custom endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/seedance-video-generation-and-editing)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)
- [AI Hive Chat and API Key Portal](https://ai-hive.iclip.cn/chat)
- [AI Hive API Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated video files downloaded by the CLI when tasks complete]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload selected media, submit potentially billable AI Hive video-generation tasks, print task JSON, and save generated MP4, MOV, or other model-supported files to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
