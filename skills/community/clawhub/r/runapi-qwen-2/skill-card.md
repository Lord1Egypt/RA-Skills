## Description:

Generate and edit images with Qwen 2 through RunAPI. Use when the user asks an agent to create, edit, or transform images with Qwen 2. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate or edit images with Qwen 2 through RunAPI, either as a one-off CLI workflow or as an SDK-backed application integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RunAPI CLI and Homebrew tap handle authentication credentials and any local media supplied for image generation or editing.

Mitigation: Confirm trust in the RunAPI tap and CLI before installation, use a scoped API key where possible, and avoid providing unrelated sensitive files.

Risk: RunAPI command help and API reference contracts may be unavailable or inconsistent for a selected operation.

Mitigation: Inspect the installed command catalog and current API reference before execution, and stop on missing facts or contract mismatches instead of guessing.

Risk: Repeated submissions can create duplicate paid tasks or hide service failures.

Mitigation: Submit each task once, persist the task response, wait on the same task ID, and only retry within the bounded recovery rules described by the artifact.

## Reference(s):

- [Qwen 2 model page](https://runapi.ai/models/qwen-2)
- [Qwen 2 model documentation](https://runapi.ai/models/qwen-2.md)
- [Alibaba provider overview](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Qwen 2 SDK integration](https://github.com/runapi-ai/qwen-2-sdk)
- [Qwen 2 edit-image variant](https://runapi.ai/models/qwen-2/edit-image.md)
- [Qwen 2 text-to-image variant](https://runapi.ai/models/qwen-2/text-to-image.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell command examples, JSON request files, and SDK integration direction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide agents to produce RunAPI task JSON, result JSON, and verified downloaded image files when the service succeeds.]

## Skill Version(s):

0.2.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
