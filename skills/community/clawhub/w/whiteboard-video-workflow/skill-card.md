## Description:

Generates a complete whiteboard animation video workflow from an SRT subtitle file by parsing scenes, generating images, producing animation segments, and merging the final video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangagent](https://clawhub.ai/user/yangagent)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, educators, marketers, and developers use this skill to turn subtitle scripts into structured storyboard data, generated whiteboard-style images, animation segments, and a merged video. It is intended for agents that can orchestrate local Python scripts, subagents, and an external image generation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subtitle-derived prompts are sent to RunningHub for image generation.

Mitigation: Avoid confidential or regulated subtitle content unless the external API use is approved.

Risk: The workflow may change local Python dependencies and relies on a separate whiteboard-animation skill.

Mitigation: Run the skill in an isolated environment with restricted filesystem access, network access, and disk quotas.

Risk: Generated image URLs are downloaded during the workflow.

Mitigation: Review and scan generated assets before reuse or publication.

Risk: The release has a suspicious security verdict in server evidence.

Mitigation: Treat installation as a reviewed decision and follow the server-provided security guidance before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangagent/skills/whiteboard-video-workflow)
- [RunningHub](https://www.runninghub.cn/)
- [RunningHub OpenAPI](https://www.runninghub.cn/openapi/v2)
- [Image Generator Reference](references/image-generator.md)
- [Storyboard Parser Reference](references/storyboard-parser.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands plus JSON status objects, storyboard files, generated image files, video segments, and a merged MP4 video.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an SRT input path, optional output directory, RunningHub API credentials, local Python dependencies, and a separate whiteboard-animation skill.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
