## Description:

Generate and edit images with Z-Image through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, edit, or transform images with RunAPI's Z-Image service, either as one-off media tasks through the CLI or as SDK-backed application integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, input images, local media paths, and API credentials may be sent to RunAPI while generating or editing images.

Mitigation: Use this skill only when RunAPI is an acceptable processor for the task data, prefer environment or saved CLI authentication, and avoid exposing unnecessary secrets or sensitive media.

Risk: The skill can trigger network requests, local file uploads, paid task submission, and output-file downloads through the RunAPI CLI.

Mitigation: Inspect the discovered operation contract before submission, submit only once per task, preserve task evidence, and verify every downloaded image is non-empty and has the expected MIME type.

Risk: A stale or mismatched CLI/API contract can cause invalid requests or misleading task behavior.

Mitigation: Treat installed command help and the current API reference as authoritative, stop on contract mismatch or missing required facts, and correct request shape only when the contract or validation error identifies the fix.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-z-image)
- [RunAPI Z-Image model page](https://runapi.ai/models/z-image)
- [RunAPI Z-Image model documentation](https://runapi.ai/models/z-image.md)
- [RunAPI Alibaba provider documentation](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Z-Image SDK](https://github.com/runapi-ai/z-image-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands, JSON request files, task/result JSON, and verified image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the runapi CLI for one-off tasks and may use RUNAPI_API_KEY or saved CLI authentication.]

## Skill Version(s):

0.2.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
