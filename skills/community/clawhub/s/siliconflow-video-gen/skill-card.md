## Description:

Generate videos using SiliconFlow API with Wan2.2 model. Supports both Text-to-Video and Image-to-Video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to submit asynchronous text-to-video or image-to-video generation jobs to SiliconFlow and receive a JSON request ID for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner verdict is suspicious because the skill uses broad command execution and passes the SiliconFlow API key to a child process command line.

Mitigation: Review before installing, use a limited SiliconFlow API key, and prefer a version that replaces curl subprocess calls with an in-process HTTPS client.

Risk: Prompts and image URLs are submitted to SiliconFlow for video generation.

Mitigation: Avoid submitting confidential prompts or private image URLs.

Risk: The documented installer is unpinned.

Mitigation: Do not run the unpinned installer with elevated privileges.

## Reference(s):

- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1)
- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/siliconflow-video-gen)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON status objects and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SiliconFlow API key and returns an asynchronous request_id instead of a completed video file.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
