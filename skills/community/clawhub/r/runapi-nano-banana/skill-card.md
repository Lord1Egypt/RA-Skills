## Description:

Generate and edit images with Nano Banana through RunAPI. Use when the user asks an agent to create, edit, or transform images with Nano Banana. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent to create, edit, or transform images with Nano Banana. Use the RunAPI CLI for one-off image work and an SDK for application or backend integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media are sent to RunAPI, and image generation may incur charges.

Mitigation: Upload only files intended for RunAPI, protect the API key, and check the model's pricing and rate limits before use.

Risk: Submitting an additional generation request after a timeout or service failure could create duplicate paid work.

Mitigation: Follow the skill's stop and recovery rules; resume waiting on the existing task and do not submit a replacement without authorization.

## Reference(s):

- [Nano Banana model overview, pricing, and rate limits](https://runapi.ai/models/nano-banana.md)
- [Google provider overview](https://runapi.ai/providers/google.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Nano Banana SDK integration](https://github.com/runapi-ai/nano-banana-sdk)
- [Nano Banana 2.1 variant](https://runapi.ai/models/nano-banana/2.1.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Generated image files with JSON request and result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image deliverables; the skill identifies image/* as the fallback media family.]

## Skill Version(s):

0.3.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
