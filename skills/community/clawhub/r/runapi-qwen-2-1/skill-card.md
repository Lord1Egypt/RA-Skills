## Description:

Generate and edit images with Qwen 2.1 through RunAPI. Use when the user asks an agent to create images, transparent-background assets, or mask-based local edits with Qwen 2.1. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover how to create images, transparent-background assets, or mask-based edits with Qwen 2.1 through RunAPI. The model is documented as upcoming, so current use is limited to checking status and read-only CLI help until a callable contract is published.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RunAPI CLI implementation is outside the supplied security review, and the model has no callable endpoints yet.

Mitigation: Use only the documented read-only help commands while the model is unavailable; check the current endpoint status and a published callable contract before submitting generation requests.

## Reference(s):

- [Qwen 2.1 model overview, pricing, and rate limits](https://runapi.ai/models/qwen-2.1.md)
- [RunAPI Alibaba provider overview](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Qwen 2.1 image editing variant](https://runapi.ai/models/qwen-2.1/edit-image.md)
- [Qwen 2.1 text-to-image variant](https://runapi.ai/models/qwen-2.1/text-to-image.md)
- [RunAPI Qwen 2.1 SDK](https://github.com/runapi-ai/qwen-2.1-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only discovery guidance and CLI help commands while the model is unavailable; no generation output is currently available.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
