## Description:

Generate music tailored to video content. Use when users request video_soundtrack operations or related tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to generate background music matched to video content through Tomoviee video soundtrack operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tomoviee API credentials may be exposed by the token generator command or generated Authorization headers.

Mitigation: Use least-privilege Tomoviee credentials, avoid printing or sharing generated tokens, and rotate credentials after testing.

Risk: Private or regulated videos may be submitted to Tomoviee/Wondershare services.

Mitigation: Submit only content approved for external processing and review Tomoviee/Wondershare data handling before use.

Risk: Bundled reference docs cover broader Tomoviee APIs beyond video background music.

Mitigation: Limit use to video soundtrack and tm_video_scoring workflows unless reviewers approve the additional APIs.

Risk: Some examples refer to a soundtrack client file while the artifact includes a video scoring client script.

Mitigation: Verify script names and imports in the installed artifact before running sample code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/tomoviee-video-background-music)
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html)
- [Tomoviee API Documentation](https://www.tomoviee.ai/doc/)
- [Tomoviee Audio Generation APIs](references/audio_apis.md)
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tomoviee API request payloads, authentication setup guidance, and async polling guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
