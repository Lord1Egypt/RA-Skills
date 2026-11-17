## Description:

Generate and edit images with Flux Kontext through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate, edit, or transform images with Flux Kontext through RunAPI. It supports one-off CLI use and SDK-based integration when the user is building an application or backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media inputs are sent to RunAPI and submitted tasks may incur provider charges.

Mitigation: Use the skill only with an authorized RunAPI account or API key, confirm authentication before submission, and submit paid requests only when the user has authorized the task.

Risk: A successful service status might not prove that the requested image deliverable is present or valid.

Mitigation: Validate the complete result contract, download every requested media deliverable, and require each downloaded file to be non-empty with the expected image MIME type before reporting completion.

Risk: An outdated CLI catalog or mismatched API contract can lead to invalid requests.

Mitigation: Inspect the installed CLI help and current API reference for the selected operation, and stop instead of guessing when the two contract sources disagree.

## Reference(s):

- [RunAPI Flux Kontext model overview](https://runapi.ai/models/flux-kontext.md)
- [RunAPI Flux Kontext homepage](https://runapi.ai/models/flux-kontext)
- [Black Forest Labs provider overview](https://runapi.ai/providers/black-forest-labs.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Flux Kontext SDK integration](https://github.com/runapi-ai/flux-kontext-sdk)
- [Flux Kontext Max variant](https://runapi.ai/models/flux-kontext/max.md)
- [Flux Kontext Pro variant](https://runapi.ai/models/flux-kontext/pro.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON request and response artifacts, and downloaded image files when generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill requires contract discovery before requests, preserves task and result JSON, and verifies downloaded image files for non-empty content and expected MIME type.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
