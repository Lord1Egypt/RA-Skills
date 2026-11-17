## Description:

Consolidates an AI agent's daily experiences and learnings into structured long-term Markdown memory through micro-rest, NREM, and REM-style consolidation modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cshiaa](https://clawhub.ai/user/cshiaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve useful session learnings, preferences, decisions, and synthesis notes across agent sessions. It supports quick within-session notes, pre-compaction flushing, end-of-session memory consolidation, and memory loading at session start.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation logs and long-term memory content may be stored indefinitely in plain Markdown.

Mitigation: Use a dedicated workspace, avoid storing secrets or regulated data, and review memory files regularly.

Risk: Raw session context or memory data may be sent to Anthropic during pre-compaction flush or sleep-cycle consolidation.

Mitigation: Run consolidation only on data approved for external processing and redact sensitive content before using API-backed modes.

Risk: Persisted memory loaded into future sessions can influence agent behavior if treated as trusted system-level context.

Mitigation: Sanitize and curate persisted memory before injecting it into high-priority prompts or system-level instructions.

## Reference(s):

- [Memory Schema Reference](references/memory_schema.md)
- [Workspace Layout Reference](references/workspace_layout.md)
- [ClawHub Skill Page](https://clawhub.ai/cshiaa/skills/sleep-consolidation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python helper scripts that read, write, or derive JSON-backed memory updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates plain Markdown memory files in the configured workspace; flush, NREM, and REM modes require an Anthropic API key.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
