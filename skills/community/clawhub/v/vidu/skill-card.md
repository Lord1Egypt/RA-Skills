## Description:

Generate AI videos using Vidu, including text-to-video, image-to-video, reference-to-video, and start-end-to-video workflows with Vidu Q3-Pro and Vidu 2.0 through Atlas Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to generate short AI videos from prompts, images, references, or paired start and end frames. It is useful for social media clips, marketing assets, product demos, anime scenes, and other video generation workflows that can be sent to Atlas Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend from the configured Atlas Cloud account because it uses ATLASCLOUD_API_KEY for generation requests.

Mitigation: Use an Atlas Cloud API key only from an account with acceptable billing exposure and review cost-related parameters before running generation.

Risk: Prompts, image URLs, video URLs, and uploaded local media can be sent to Atlas Cloud.

Mitigation: Use only prompts and media that are acceptable to share with Atlas Cloud, and review local files before using the upload command.

Risk: The Vidu-focused description is narrower than the bundled script behavior, which can access broader Atlas Cloud video models.

Mitigation: Confirm the selected model ID before submission and restrict usage to intended Vidu models when that is the expected workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/vidu)
- [Publisher profile](https://clawhub.ai/user/xixihhhh)
- [Atlas Cloud](https://www.atlascloud.ai)
- [Atlas Cloud video generation API](https://api.atlascloud.ai/api/v1/model/generateVideo)
- [fal.ai Vidu Q3-Pro pricing reference](https://fal.ai/models/fal-ai/vidu/q3-pro/text-to-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python script usage, API request examples, and generated video file paths or URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or download MP4 video files after sending prompts, image URLs, video URLs, or uploaded local media to Atlas Cloud.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
