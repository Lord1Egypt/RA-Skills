## Description:

Generate and edit images with Qwen 3 through RunAPI for agent workflows that need image creation, transformation, or SDK integration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent prepare, submit, and verify Qwen 3 image generation or image editing tasks through RunAPI. For application integration, the skill directs agents to use the current RunAPI SDK reference instead of shelling out from production code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit paid RunAPI tasks.

Mitigation: Authenticate before submission, submit exactly once, and avoid replacement submissions without user authorization.

Risk: Local media paths included in requests may be uploaded to RunAPI.

Mitigation: Include only user-intended media inputs and validate request JSON before execution.

Risk: Authentication may require a RunAPI API key or saved CLI login.

Mitigation: Prefer environment or saved CLI authentication, and use browser login only when the user explicitly requests it.

Risk: A successful task status may not prove the requested deliverable is usable.

Mitigation: Validate the full result contract and require non-empty downloaded files with the expected image MIME type.

## Reference(s):

- [Qwen 3 model overview](https://runapi.ai/models/qwen-3.md)
- [RunAPI Qwen 3 homepage](https://runapi.ai/models/qwen-3)
- [Alibaba provider overview](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Qwen 3 SDK integration](https://github.com/runapi-ai/qwen-3-sdk)
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-qwen-3)
- [RunAPI publisher profile](https://clawhub.ai/user/runapi-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request files, SDK integration code, and verified image deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create request, task, result, error, and downloaded image files in the working directory.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
