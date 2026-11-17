## Description:

Captures learnings, errors, and corrections so agents can record user feedback, command failures, knowledge gaps, feature requests, and reusable workflow improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve useful corrections, debugging lessons, command failures, and requested capabilities in local Markdown learning logs. It also supports optional reminder hooks and skill extraction for recurring, broadly useful learnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted guidance can carry incorrect, stale, or over-broad instructions into future agent sessions.

Mitigation: Review entries before promotion and keep durable guidance scoped to the relevant project, workflow, or tool.

Risk: Learning logs, hook inputs, or copied command output may contain secrets, raw transcripts, environment values, or sensitive source/configuration details.

Mitigation: Record short sanitized summaries, redact sensitive values, and avoid logging raw transcripts or full command output unless explicitly required.

Risk: Broad or global hook configuration can inject reminders into unrelated sessions and increase exposure to unnecessary context.

Mitigation: Prefer project-scoped hooks, use the minimal activator-only setup by default, and enable error-detection hooks only in trusted environments.

Risk: Skill extraction can create reusable guidance from a one-off incident before it is verified or broadly applicable.

Mitigation: Use the documented extraction criteria, run dry-run scaffolding first, and verify the new skill content before relying on it.

## Reference(s):

- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional hook configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning-log entries and scaffolding guidance; optional hooks emit reminder text.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
