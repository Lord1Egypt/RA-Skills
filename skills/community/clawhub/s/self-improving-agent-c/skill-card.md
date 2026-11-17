## Description:

Captures learnings, errors, and corrections to enable continuous improvement for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhaoyu521](https://clawhub.ai/user/chenhaoyu521)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and reusable learnings in structured markdown files for later review or promotion into trusted project guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and prompt-memory promotion can carry incorrect or misleading guidance into later agent sessions.

Mitigation: Require human review before promoting entries into agent instruction files or extracting new skills.

Risk: Optional hooks with broad triggers can affect many sessions or workspaces.

Mitigation: Prefer project-local hook configuration and activator-only setup; avoid global or broad empty-match hooks unless all affected workspaces are trusted.

Risk: Error-detection hooks may inspect command output that includes sensitive information.

Mitigation: Redact secrets before logging and avoid storing raw transcripts, environment variables, tokens, or full command output.

## Reference(s):

- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and structured log-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends project-local .learnings markdown files when used as directed; optional hooks emit reminder text during agent lifecycle events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
