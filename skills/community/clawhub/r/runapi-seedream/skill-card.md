## Description:

Generate and edit images with Seedream through RunAPI. Use when the user asks an agent to create, edit, or transform images with Seedream. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate, edit, transform, and verify image outputs with Seedream through RunAPI. It supports one-off CLI use and SDK-based application integration while requiring contract discovery before requests are submitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected local media files may be sent to RunAPI/Seedream.

Mitigation: Review request content and local file paths before submission, and send only files the user intended to process.

Risk: RunAPI model calls require authentication and may be billable.

Mitigation: Keep API keys in environment variables or the CLI auth flow, verify authentication before submitting, and avoid replacement paid requests without user authorization.

Risk: Media deliverables may be missing, empty, or have an unexpected MIME type if response verification is skipped.

Mitigation: Download every requested media deliverable and verify non-empty files with the expected image MIME family before reporting completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-seedream)
- [RunAPI Seedream homepage](https://runapi.ai/models/seedream)
- [Seedream model overview, pricing, and rate limits](https://runapi.ai/models/seedream.md)
- [ByteDance provider overview](https://runapi.ai/providers/bytedance.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Seedream SDK integration](https://github.com/runapi-ai/seedream-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce request and response files, downloaded image deliverables, and SDK integration code when requested.]

## Skill Version(s):

0.2.11 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
