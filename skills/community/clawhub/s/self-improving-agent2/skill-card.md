## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents across command failures, user corrections, missing capabilities, external tool failures, outdated knowledge, and recurring task improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashi6174](https://clawhub.ai/user/dashi6174)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to capture corrections, errors, feature requests, and reusable learnings in structured Markdown logs. It also provides optional hook guidance for reminding agents to record and promote broadly useful learnings into workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived guidance may be persisted into future agent instruction files or workspace memory.

Mitigation: Keep learning logs project-local, sanitize entries, and require manual review before promoting learnings into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Optional hooks can run broadly and inspect command output for error patterns.

Mitigation: Enable hooks only in trusted environments, prefer the lightweight activator hook by default, and review scripts before enabling global or PostToolUse hooks.

Risk: Logs can accidentally capture secrets, raw transcripts, environment variables, or sensitive command output.

Mitigation: Record short sanitized summaries or redacted excerpts, and avoid forwarding or storing raw transcripts and full command output unless explicitly approved.

## Reference(s):

- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-local learning logs, optional hook reminders, and skill-scaffold guidance; avoid storing secrets, raw transcripts, or full command output unless explicitly approved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
