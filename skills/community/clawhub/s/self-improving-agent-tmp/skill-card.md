## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents across OpenClaw and other agent frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelaner](https://clawhub.ai/user/kelaner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record failures, corrections, feature requests, and reusable practices so future sessions can apply or promote those learnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted learning records can carry user or agent context into future sessions and broad agent instruction files.

Mitigation: Review entries before promotion and require explicit review before writing to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Broad hook configuration, especially global hooks or empty matchers, can affect every prompt.

Mitigation: Prefer project-scoped hooks, use narrower matchers when possible, and keep hook setup opt-in.

Risk: Learning logs can accidentally store secrets, personal data, raw transcripts, or raw tool output.

Mitigation: Do not store sensitive content in .learnings, and only use sessions_history or sessions_send after the user approves the specific source and destination.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces learning logs, error entries, feature-request entries, promotion guidance, hook reminders, and optional skill scaffolds.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
