## Description:

Generate and edit images and videos with Grok Imagine through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide agents through one-off Grok Imagine image and video generation, media editing, and SDK integration through RunAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RunAPI CLI may make authenticated and billable service requests.

Mitigation: Use the skill only when RunAPI/Grok Imagine usage is intended, authenticate with approved credentials, and preserve task responses before waiting or retrying.

Risk: Generated media files are downloaded from remote service responses and may be unsafe to open blindly.

Mitigation: Treat downloaded outputs as untrusted media files and verify that each file is non-empty and has the expected MIME type before reporting completion.

Risk: Supplying unsupported request fields or guessing missing contract details can lead to failed or unintended service requests.

Mitigation: Inspect the installed command help and current API reference, build requests only from accepted fields, and stop when the contract is missing or contradictory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-grok-imagine)
- [RunAPI Grok Imagine homepage](https://runapi.ai/models/grok-imagine)
- [Grok Imagine model documentation](https://runapi.ai/models/grok-imagine.md)
- [xAI provider documentation](https://runapi.ai/providers/xai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Grok Imagine SDK integration](https://github.com/runapi-ai/grok-imagine-sdk)
- [Edit image variant](https://runapi.ai/models/grok-imagine/edit-image.md)
- [Image 2.0 variant](https://runapi.ai/models/grok-imagine/image-2-0.md)
- [Image-to-video variant](https://runapi.ai/models/grok-imagine/image-to-video.md)
- [Text-to-image variant](https://runapi.ai/models/grok-imagine/text-to-image.md)
- [Text-to-video variant](https://runapi.ai/models/grok-imagine/text-to-video.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to create request JSON, execute RunAPI CLI or SDK workflows, and verify downloaded image or video files.]

## Skill Version(s):

0.2.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
