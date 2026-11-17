## Description:

Automates a YouTube Shorts pipeline that creates short vertical videos with Deevid AI Agent and uploads them to YouTube.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangjjang](https://clawhub.ai/user/kangjjang)

### License/Terms of Use:


## Use Case:

Content creators and channel operators use this skill to generate 9:16 AI-assisted Shorts, configure upload metadata, publish with YouTube OAuth, and optionally run the workflow on a daily schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploads may publish publicly even when private or unlisted visibility is requested.

Mitigation: Fix or remove the broken privacy option, then confirm upload visibility and target channel before publishing.

Risk: OAuth client secrets and tokens may expose YouTube upload access if stored in shared folders or source control.

Mitigation: Keep OAuth files outside shared locations, exclude them from source control, and rotate credentials if exposure is suspected.

Risk: Scheduled runs can repeatedly publish generated content without a final human visibility check.

Mitigation: Enable scheduling only after publication visibility, channel identity, and content review expectations are explicit.

## Reference(s):

- [Deevid Agent Video Generation Workflow](references/deevid-agent-workflow.md)
- [YouTube Shorts Upload](references/youtube-upload.md)
- [Channel Configuration Example](references/config_example.json)
- [Deevid Agent](https://deevid.ai/ko/agent)
- [Deevid AI](https://deevid.ai/ko/)
- [YouTube Shorts Output URL Pattern](https://youtube.com/shorts/{video_id})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference OAuth credential files, generated video files, and scheduled execution settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
