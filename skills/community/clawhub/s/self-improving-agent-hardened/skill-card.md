## Description:

Captures learnings, errors, corrections, and feature requests as local markdown records, with anti-loop guardrails that limit each trigger to one learning and prevent chained self-improvement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record command failures, explicit user corrections, missing capabilities, and external tool issues for later review. It is intended for local learning workflows where entries are written to .learnings/ markdown files and promotion is deferred until a user-initiated review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning records can influence future agent behavior.

Mitigation: Review each learning before promotion and keep promotion user-initiated.

Risk: Optional prompt and tool hooks can apply broadly when configured globally.

Mitigation: Prefer project-scoped hooks and minimal hook configuration; avoid global UserPromptSubmit setup unless the broader behavior is intended.

Risk: Learning entries may capture sensitive context from failures, corrections, or tool output.

Mitigation: Redact secrets, credentials, private data, and unnecessary user details before writing or promoting entries.

Risk: The README replacement install example removes an existing skill directory.

Mitigation: Use a backup or staged install flow pinned to a reviewed version instead of a direct removal command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/self-improving-agent-hardened)
- [README](README.md)
- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file-entry templates, shell commands, and hook configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or scaffolds local markdown learning records when the agent follows the skill; optional hooks emit reminder text.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
