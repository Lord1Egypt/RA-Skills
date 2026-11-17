## Description:

Generates 5-second videos from image and text prompts using the Tomoviee Image-to-Video API through the Wondershare OpenAPI gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to animate still images with prompt and camera-motion guidance through Tomoviee's image-to-video API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Tomoviee app credentials can be exposed through command-line examples, shell history, terminal logs, CI logs, or agent transcripts.

Mitigation: Use a secret manager or environment-based injection for live credentials, avoid the auth helper with production secrets, and rotate credentials that may have appeared in logs.

Risk: Image URLs, prompts, and callback data are sent to a third-party API gateway for processing.

Mitigation: Submit only approved images and URLs, avoid private or sensitive assets unless third-party processing is authorized, and review endpoint egress before deployment.

## Reference(s):

- [Tomoviee Image-to-Video API Reference](references/video_apis.md)
- [Camera Movement Types Reference](references/camera_movements.md)
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md)
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html)
- [Tomoviee Image-to-Video API Docs](https://www.tomoviee.ai/doc/ai-video/image-to-video.html)
- [Tomoviee Mainland Developer Portal](https://www.tomoviee.cn/developers.html)
- [Tomoviee Mainland Image-to-Video API Docs](https://www.tomoviee.cn/doc/ai-video/image-to-video.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, polling status, and video URLs when the API client is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
