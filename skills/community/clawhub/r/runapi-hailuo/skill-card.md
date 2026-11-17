## Description:

Generate and edit video with Hailuo through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, edit, or transform video with Hailuo through RunAPI. It guides one-off CLI generation and SDK-based application integration while requiring contract discovery and output verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use of RunAPI can involve paid Hailuo generation tasks and uploaded media.

Mitigation: Confirm authorization, pricing, authentication state, and intended media inputs before submitting a task.

Risk: A stale or mismatched operation contract can lead to invalid requests or incorrect assumptions about results.

Mitigation: Inspect the installed command help and current API contract, and stop if those sources disagree.

Risk: A successful task status may still omit requested media or return an unexpected file type.

Mitigation: Validate the complete response, download every requested deliverable, and require non-empty files with the expected video MIME family.

## Reference(s):

- [Hailuo model overview](https://runapi.ai/models/hailuo.md)
- [RunAPI Hailuo homepage](https://runapi.ai/models/hailuo)
- [Minimax provider overview](https://runapi.ai/providers/minimax.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Hailuo SDK integration](https://github.com/runapi-ai/hailuo-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to preserve task/result JSON and verify downloaded video deliverables.]

## Skill Version(s):

0.2.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
