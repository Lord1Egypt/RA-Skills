## Description:

Captures errors, corrections, feature requests, and recurring workflow improvements so OpenClaw agents can keep durable learning logs and avoid repeating mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sam-k-migz](https://clawhub.ai/user/sam-k-migz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record sanitized learnings, command failures, corrections, and feature requests in workspace logs, then promote broadly useful lessons into persistent agent guidance with review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad logging and promotion into persistent agent instructions can introduce noisy, sensitive, or incorrect guidance.

Mitigation: Keep hooks project-scoped, log sanitized summaries only, and require explicit approval with an exact diff before writing to AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Error-detection hooks may inspect command output that contains sensitive data.

Mitigation: Enable the error detector only in trusted workspaces and avoid storing secrets, tokens, private keys, environment variables, or full transcripts.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup](references/hooks-setup.md)
- [Usage Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured log-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace learning logs and may propose reviewed promotion into persistent agent instruction files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
