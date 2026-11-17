## Description:

Generate and edit images, create or extend video from images, derive or shorten prompt suggestions, and look up seeds with Midjourney through RunAPI, using the RunAPI CLI for one-off work and language SDKs for application integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform Midjourney generation, editing, video, prompt, and seed tasks through RunAPI as either one-off CLI jobs or SDK-backed application integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input media may be sent to RunAPI.

Mitigation: Use only approved inputs and avoid sending sensitive or proprietary media unless that data sharing is authorized.

Risk: Generated RunAPI jobs may incur costs.

Mitigation: Submit each job once, retry only under the skill's stated safe-retry conditions, and get user authorization before replacing a paid request.

Risk: API credentials could be exposed if handled directly in prompts, files, or logs.

Mitigation: Use RUNAPI_API_KEY or a trusted CLI auth flow, and avoid embedding credentials in request files or command output.

Risk: A request can become invalid if the installed CLI contract and API reference differ or change.

Mitigation: Inspect the current CLI help and API reference before building requests, and stop on contract mismatches instead of guessing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-midjourney)
- [RunAPI Midjourney model homepage](https://runapi.ai/models/midjourney)
- [RunAPI Midjourney model documentation](https://runapi.ai/models/midjourney.md)
- [RunAPI Midjourney provider overview](https://runapi.ai/providers/midjourney.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Midjourney SDK](https://github.com/runapi-ai/midjourney-sdk)
- [Midjourney edit image variant](https://runapi.ai/models/midjourney/edit-image.md)
- [Midjourney image to video variant](https://runapi.ai/models/midjourney/image-to-video.md)
- [Midjourney v8.1 variant](https://runapi.ai/models/midjourney/v8.1.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request files, SDK integration direction, and validation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or verify image and video media deliverables through RunAPI responses.]

## Skill Version(s):

0.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
