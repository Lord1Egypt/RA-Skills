## Description:

Generates 5-second videos from text prompts through the Tomoviee Text-to-Video API with controls for resolution, aspect ratio, and camera movement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative automation users use this skill to generate short text-to-video assets via the Tomoviee/Wondershare API, tune resolution, aspect ratio, and camera movement, and retrieve generated video URLs from asynchronous tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be exposed if app keys, app secrets, or generated Basic tokens are entered directly in shell commands or printed to logs.

Mitigation: Use secure prompts, environment injection configured not to log values, or a secret manager; rotate credentials if they were exposed.

Risk: Prompts and generation requests are sent to the Tomoviee/Wondershare OpenAPI gateway.

Mitigation: Review prompts for sensitive or regulated content before submission and apply organizational data-sharing controls.

## Reference(s):

- [Tomoviee Video Generation APIs](references/video_apis.md)
- [Camera Movement Types Reference](references/camera_movements.md)
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md)
- [Tomoviee Developer Portal (Global)](https://www.tomoviee.ai/developers.html)
- [Tomoviee API Docs (Global)](https://www.tomoviee.ai/doc/)
- [Tomoviee Developer Portal (Mainland)](https://www.tomoviee.cn/developers.html)
- [Tomoviee API Docs (Mainland)](https://www.tomoviee.cn/doc/)
- [Wondershare OpenAPI Gateway](https://openapi.wondershare.cc)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs and video URLs returned by Tomoviee API; generated videos are limited to 5 seconds.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
