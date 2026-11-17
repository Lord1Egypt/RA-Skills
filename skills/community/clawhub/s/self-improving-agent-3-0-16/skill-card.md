## Description:

Captures learnings, errors, corrections, and feature requests so agents can maintain durable improvement logs and review them before future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngsiai](https://clawhub.ai/user/youngsiai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, and requested capabilities in structured learning files. It also provides optional hook guidance for reminder-based capture and promotion of reviewed learnings into agent instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores conversation-derived learnings that may include sensitive content if used carelessly.

Mitigation: Keep `.learnings` local by default, redact secrets and private data, and prefer short summaries over raw transcripts or full command output.

Risk: Promoting entries into agent instruction files can carry incorrect or unreviewed guidance into future sessions.

Mitigation: Require review of every entry and approve the exact text before writing to `CLAUDE.md`, `AGENTS.md`, `SOUL.md`, `TOOLS.md`, or Copilot instructions.

Risk: Optional hooks can inspect command output and reinforce logging behavior automatically.

Mitigation: Enable hooks only in trusted environments, use the activator-only setup by default, and add error-pattern hooks only after reviewing their behavior.

## Reference(s):

- [Skill README](README.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/youngsiai/skills/self-improving-agent-3-0-16)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning, error, and feature-request entries when the agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
