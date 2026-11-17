## Description:

Intelligent session compression plugin for OpenClaw that automatically manages token consumption and supports unlimited-length conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdc-creator](https://clawhub.ai/user/sdc-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to compact long conversation histories into structured summaries, monitor token usage, and manage compaction behavior through CLI commands and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell invocation may expose command execution risk when prompts are passed to OpenClaw through a shell command.

Mitigation: Replace shell-based execution with non-shell argument execution before use with sensitive conversations or credentials.

Risk: Debug logging can expose configuration values.

Mitigation: Remove debug config logging or redact sensitive fields before deployment.

Risk: Session-file access can be unsafe if session identifiers are not strictly constrained.

Mitigation: Validate session IDs and restrict reads and writes to the intended OpenClaw session directory.

Risk: Automatic compaction rewrites conversation history and can hide or distort context.

Mitigation: Give users explicit control over automatic compaction and provide summary review for sensitive workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdc-creator/skills/session-compact-skill)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Release Notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, CLI status text, shell commands, and OpenClaw JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May automatically summarize and replace older session history while preserving recent messages.]

## Skill Version(s):

1.2.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
