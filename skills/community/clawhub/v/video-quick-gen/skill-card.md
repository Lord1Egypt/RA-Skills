## Description:

营销视频生成服务，通过小念AI的视频模块快速生成营销视频：当用户说"快速生成视频/生成一个视频/做个视频/把这个需求直接生成视频"并希望通过小念AI生成结果而不是手动编写时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yc556600](https://clawhub.ai/user/yc556600)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a marketing video request into a generated script and video through Xiaonian AI's video API. The skill returns the generated script, task status, final video URL, and optionally a downloaded local video file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships with and automatically uses a reusable bearer token.

Mitigation: Require each user to provide their own secret at runtime and remove any shared token from the release artifact.

Risk: The bearer token can be sent to a configured server outside the intended service.

Mitigation: Restrict the API origin to the intended Xiaonian HTTPS endpoint before use.

Risk: Marketing or business details submitted in prompts may be sent to the video-generation API.

Mitigation: Avoid sensitive campaign or business inputs until authentication and endpoint handling are fixed and reviewed.

## Reference(s):

- [Video Gen API](artifact/references/video-api.md)
- [ClawHub skill page](https://clawhub.ai/yc556600/skills/video-quick-gen)
- [Xiaonian dashboard service](https://xiaonian.cc)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON containing task state, generated script text, video URL, and optional local download path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download the generated video to a local file when an output path is provided.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
