## Description:

Generates videos with the Volcengine SD1.5pro API from text prompts or image references, polls asynchronous tasks, and downloads the resulting MP4 file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronzoe](https://clawhub.ai/user/aaronzoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to submit text-to-video or image-to-video requests to Volcengine SeeDance-compatible SD1.5pro model endpoints and save the generated video locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and related generation metadata are sent to Volcengine.

Mitigation: Use only inputs that are appropriate to share with Volcengine and review provider terms before use.

Risk: The required config.json contains a live API key.

Mitigation: Store config.json carefully, avoid committing or sharing it, and rotate the key if exposure is suspected.

Risk: Generated MP4 files are written to the configured or default output path.

Mitigation: Choose an explicit output path when you need control over where generated videos are saved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronzoe/skills/video-generator-seedance)
- [Volcengine API documentation](https://www.volcengine.com/docs/)
- [Volcengine console](https://console.volcengine.com/)

## Skill Output:

**Output Type(s):** [shell commands, configuration, files, guidance]

**Output Format:** [CLI output and local MP4 file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Volcengine API key and model ID in config.json; accepts a prompt, optional image URL, duration, output path, camera-fixed flag, and watermark flag.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
