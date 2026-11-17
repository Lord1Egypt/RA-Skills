## Description:

Generate video with sound from text, a first-frame image, or reference media with HeyGen Video through RunAPI. Use the RunAPI CLI for one-off generation and an SDK for application integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other creators use this skill to generate videos with sound from text or media through RunAPI, either as one-off results or within applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media selected for generation may be uploaded to RunAPI/HeyGen.

Mitigation: Review local media paths and content before submitting a request.

Risk: Generation requests may incur charges; authentication grants access to a RunAPI account.

Mitigation: Use a trusted RunAPI account and approve any additional paid request beyond the first task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/runapi-ai/skills/runapi-heygen-video)
- [HeyGen Video model overview](https://runapi.ai/models/heygen-video)
- [HeyGen Video model details and pricing](https://runapi.ai/models/heygen-video.md)
- [HeyGen provider overview](https://runapi.ai/providers/heygen.md)
- [HeyGen Video SDK integration](https://github.com/runapi-ai/heygen-video-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with shell commands and JSON request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides video retrieval and verification after generation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
