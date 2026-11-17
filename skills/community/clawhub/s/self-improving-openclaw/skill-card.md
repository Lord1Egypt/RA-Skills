## Description:

Log corrections, errors, feature requests, and recurring patterns into structured workspace learning files, then promote stable patterns into tiered memory and OpenClaw workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muhamadbasim](https://clawhub.ai/user/muhamadbasim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain a structured local learning loop for corrections, errors, feature requests, recurring patterns, and heartbeat review. It helps agents capture raw lessons, review recurrence, and promote stable patterns into workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived content may become persistent agent memory or behavior without adequate review.

Mitigation: Require explicit approval before promoting entries into HOT.md, AGENTS.md, SOUL.md, TOOLS.md, or MEMORY.md.

Risk: Raw learning entries may contain untrusted, sensitive, or incorrect content.

Mitigation: Treat raw entries as untrusted until reviewed, redact secrets, avoid sensitive personal data, and keep memory files in private local workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/muhamadbasim/skills/self-improving-openclaw)
- [OpenClaw Homepage](https://github.com/muhamadbasim/oktoclaw)
- [Logging Format](references/logging-format.md)
- [Promotion and Demotion Rules](references/promotion-rules.md)
- [Heartbeat Review Procedure](references/heartbeat-review.md)
- [Workspace Layout](references/workspace-layout.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initializes and maintains local workspace memory files under .learnings/ and .self-improving/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
