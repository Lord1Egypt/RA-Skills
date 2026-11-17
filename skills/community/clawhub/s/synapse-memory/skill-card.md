## Description:

Synapse is a self-learning memory skill for OpenClaw agents that analyzes interactions, extracts preferences and patterns, updates local profiles, and improves cross-session recall using OpenClaw memory tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadoprizm](https://clawhub.ai/user/shadoprizm)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use Synapse to help agents maintain local structured memory about facts, preferences, behavioral patterns, and corrections across sessions. It is intended for agents that need improved recall while continuing to use OpenClaw's native memory_search and memory_get tools as the primary memory read path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can build long-lived profiles from conversations, preferences, and behavioral patterns.

Mitigation: Restrict transcript access where possible, require confirmation before saving inferred memories, and periodically inspect the local Synapse memory directory.

Risk: Quiet learning can save sensitive or incorrect inferred memories if agent controls are too permissive.

Mitigation: Do not store passwords, API keys, tokens, or sensitive credentials; review memory writes and use low confidence when evidence is uncertain.

Risk: Package-name mismatch could lead to installing an unintended release.

Mitigation: Install only the exact reviewed ClawHub release, shadoprizm/synapse-memory version 1.1.0.

## Reference(s):

- [Synapse ClawHub listing](https://clawhub.ai/shadoprizm/skills/synapse-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Agent guidance with local JSON, JSONL, and Markdown memory file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local OpenClaw memory files and may write profile, preference, pattern, daily log, and association records.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
