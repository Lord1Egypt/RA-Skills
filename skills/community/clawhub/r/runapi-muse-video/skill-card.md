## Description:

Generate video from a text prompt or one source image with Muse Video through RunAPI. Use the RunAPI CLI for one-off generation and an SDK for application integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate video from a text prompt or a single source image through RunAPI, using the CLI for one-off work or an SDK for application integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to RunAPI, so sensitive media may be exposed to the service.

Mitigation: Review RunAPI privacy terms before using sensitive prompts or images.

Risk: Video generation may incur charges, including during retries.

Mitigation: Check current pricing and rate limits, and keep retries within the documented limits.

Risk: A RunAPI API key could be exposed if handled insecurely.

Mitigation: Protect the key and prefer environment authentication or saved CLI configuration.

Risk: External dependency behavior was not audited, and linked live model documentation could not be retrieved.

Mitigation: Review current RunAPI model documentation and dependency behavior before relying on the workflow.

## Reference(s):

- [Muse Video model overview, pricing, and rate limits](https://runapi.ai/models/muse-video.md)
- [RunAPI Meta provider overview](https://runapi.ai/providers/meta.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Muse Video SDK](https://github.com/runapi-ai/muse-video-sdk)

## Skill Output:

**Output Type(s):** [Video files, JSON, Shell commands, Guidance]

**Output Format:** [Generated video media with JSON task results and Markdown workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-video and image-to-video with one source image.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
