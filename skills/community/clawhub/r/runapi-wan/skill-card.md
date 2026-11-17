## Description:

Generate and edit video with Wan through RunAPI. Use when the user asks an agent to create, edit, or transform video with Wan. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate, edit, or transform video with Wan through RunAPI, either as a one-off CLI workflow or as guidance for SDK integration in an application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can submit paid RunAPI tasks and send prompts or referenced media files to RunAPI/Wan.

Mitigation: Confirm authentication, request shape, and user authorization before submission; submit once and avoid repeat paid requests without explicit approval.

Risk: Generated deliverables are downloaded from URLs returned by the service and should be treated as untrusted media files.

Mitigation: Download every requested deliverable, require non-empty files and expected MIME types, and review generated media before use.

Risk: A missing CLI service, stale command catalog, or API contract mismatch can lead to incorrect execution guidance.

Mitigation: Inspect the installed CLI help and current RunAPI API reference before execution, and stop on unresolved contract mismatches instead of guessing.

## Reference(s):

- [RunAPI Wan model overview](https://runapi.ai/models/wan.md)
- [RunAPI Wan homepage](https://runapi.ai/models/wan)
- [RunAPI Alibaba provider overview](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Wan SDK](https://github.com/runapi-ai/wan-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request/response file examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce RunAPI task/result JSON and downloaded image or video deliverables when executed by an agent.]

## Skill Version(s):

0.2.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
