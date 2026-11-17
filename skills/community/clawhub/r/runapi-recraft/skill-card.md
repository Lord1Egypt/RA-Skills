## Description:

Generate and edit images with Recraft through RunAPI for one-off image tasks or SDK-based application integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to generate, edit, transform, and verify Recraft image outputs through RunAPI. Application teams use it as guidance for integrating Recraft with RunAPI SDKs instead of shelling out to the CLI in production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill may upload local media files included in RunAPI requests.

Mitigation: Use it only with media the user intends to send to RunAPI/Recraft and review request files before submission.

Risk: RunAPI authentication may be required before submitting a task.

Mitigation: Prefer saved CLI authentication or RUNAPI_API_KEY, and ask the user before using interactive browser login.

Risk: Image-generation tasks may incur paid submissions or produce incomplete media deliverables.

Mitigation: Submit once, preserve task evidence, wait on the same task, and verify every downloaded deliverable is non-empty and has the expected MIME type before reporting completion.

## Reference(s):

- [RunAPI Recraft homepage](https://runapi.ai/models/recraft)
- [Recraft model overview, pricing, and rate limits](https://runapi.ai/models/recraft.md)
- [Recraft provider overview](https://runapi.ai/providers/recraft.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Recraft SDK](https://github.com/runapi-ai/recraft-sdk)
- [Recraft crisp upscale variant](https://runapi.ai/models/recraft/crisp-upscale.md)
- [Recraft remove background variant](https://runapi.ai/models/recraft/remove-background.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files, Code]

**Output Format:** [Markdown guidance with shell commands, JSON request and response files, downloaded media files, and optional SDK code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the RunAPI CLI and optional RUNAPI_API_KEY authentication; the skill directs agents to verify generated media files before reporting completion.]

## Skill Version(s):

0.2.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
