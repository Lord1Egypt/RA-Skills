## Description:

Generate video from text, reference media, or first and last frames with MiniMax H3 through RunAPI. Use the RunAPI CLI for one-off generation and an SDK for application integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create MiniMax H3 video-generation requests through RunAPI, submit one-off tasks with the CLI, or integrate the same workflow through an SDK in application code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external RunAPI CLI, Homebrew tap, and SDK before submitting network requests.

Mitigation: Confirm trust in RunAPI's distribution sources before installing or integrating them.

Risk: RunAPI credentials may be needed for authenticated generation tasks.

Mitigation: Prefer environment authentication or saved CLI configuration and use a narrowly scoped API key where possible.

Risk: Video-generation tasks may incur paid service costs or create billable tasks.

Mitigation: Review costs before submission, submit only once by default, and avoid replacement paid requests without user authorization.

Risk: Generated media deliverables can be incomplete, empty, or have an unexpected media type.

Mitigation: Download every requested media result and verify each file is non-empty with the expected video/* MIME family before reporting completion.

## Reference(s):

- [MiniMax H3 model overview, pricing, and rate limits](https://runapi.ai/models/minimax-h3.md)
- [RunAPI MiniMax provider overview](https://runapi.ai/providers/minimax.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [MiniMax H3 SDK integration](https://github.com/runapi-ai/minimax-h3-sdk)
- [MiniMax H3 homepage](https://runapi.ai/models/minimax-h3)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Files]

**Output Format:** [Markdown guidance with shell commands, JSON request and response files, SDK integration notes, and downloaded video deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the runapi CLI for one-off use and may use RUNAPI_API_KEY or saved RunAPI authentication. The expected media output family is video/*.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
