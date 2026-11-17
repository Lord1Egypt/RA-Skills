## Description:

字幕菌 (zimujun) extracts transcript or subtitle text from mainstream video platform links, including YouTube, TikTok/Douyin, Xiaohongshu, and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a video URL or shared video text into a transcript-style result. It normalizes the URL, invokes the zimujun npm package, and returns the extracted text or the service error.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation suggests sending ZMJ_API_KEY through chat in one fallback path.

Mitigation: Do not paste the API key into chat; configure ZMJ_API_KEY locally through a secure environment or secret manager.

Risk: The skill runs zimujun@latest from the live npm registry.

Mitigation: Prefer a pinned package version or a reviewed local installation before using the skill in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyriswu/skills/zimujun)
- [Web transcript entry point](https://devtool.uk/video-transcript)
- [API key information](https://devtool.uk/plugin)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown result with video_url, status, transcript content, and error text when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npx, the zimujun npm package, and a locally configured ZMJ_API_KEY.]

## Skill Version(s):

1.0.18 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
