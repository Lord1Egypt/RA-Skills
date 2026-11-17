## Description:

Consolidate daily session logs into L2 topic files and a compact MEMORY.md index, in three bounded phases with backups, lifecycle and secret guards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzyling](https://clawhub.ai/user/lzyling)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to turn daily session logs into curated topic notes and a compact memory index, manually or on a schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual or scheduled runs can rewrite persistent workspace memory.

Mitigation: Use an explicit prompt or carefully reviewed schedule and retain backups before running.

Risk: Sensitive non-credential details in daily logs may be promoted into durable notes.

Mitigation: Apply stricter privacy rules when needed and review curated memory for sensitive content.

## Reference(s):

- [Signal Dreaming on ClawHub](https://clawhub.ai/lzyling/skills/signal-dreaming)
- [Dream protocol](references/dream-protocol.md)
- [Memory stack](references/memory-stack.md)
- [Dream audit](references/dream-audit.sh)

## Skill Output:

**Output Type(s):** [Markdown files, Text summary]

**Output Format:** [Markdown memory index, topic notes and dream log; plain-text run summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps daily logs read-only and backs up existing memory files before editing.]

## Skill Version(s):

5.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
