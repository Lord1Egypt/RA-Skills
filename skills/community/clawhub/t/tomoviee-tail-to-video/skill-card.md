## Description:

Generates 5-second videos from first and last frame image URLs using the Tomoviee First-Last Frame API through the Wondershare OpenAPI gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Tomoviee first-last frame video generation requests, including authentication, request parameters, polling, and parsing the returned video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication helper can expose reusable Tomoviee/Wondershare credentials through command-line arguments and terminal output.

Mitigation: Avoid the helper for real credentials; pass secrets through a controlled secret manager or private runtime configuration and keep them out of shells, CI logs, and agent transcripts.

Risk: Prompts and image URLs are sent to Wondershare/Tomoviee endpoints during generation.

Mitigation: Use only non-sensitive prompts and image URLs that are acceptable to share with the third-party service.

Risk: Callback URLs and passthrough parameters may disclose internal endpoints or sensitive metadata.

Mitigation: Use externally safe callback URLs and sanitize passthrough parameters before including them in API requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/tomoviee-tail-to-video)
- [Tomoviee First-Last Frame to Video API reference](references/video_apis.md)
- [Camera Movement Types Reference](references/camera_movements.md)
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md)
- [Tomoviee developer portal](https://www.tomoviee.ai/developers.html)
- [Tomoviee first-and-last-frame API documentation](https://www.tomoviee.ai/doc/ai-video/first-and-last-frame-to-video.html)
- [Tomoviee mainland developer portal](https://www.tomoviee.cn/developers.html)
- [Tomoviee mainland first-and-last-frame API documentation](https://www.tomoviee.cn/doc/ai-video/first-and-last-frame-to-video.html)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with Python and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Tomoviee task IDs and video URLs when used with valid credentials.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
