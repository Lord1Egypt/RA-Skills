## Description:

Context Manager helps agents manage local layered memory with model-aware context limits, dynamic memory loading, and SQLite-backed storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q012315](https://clawhub.ai/user/q012315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to initialize a local memory store, add memories, inspect context statistics, and adapt memory handling to model context limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memories may contain sensitive information and are stored locally in plaintext at a predictable ~/.openclaw path.

Mitigation: Do not store passwords, tokens, private conversations, or business-sensitive data, and review local memory files before sharing or disposing of an environment.

Risk: Some documented memory-management features may be unavailable in the current implementation.

Mitigation: Validate required commands in a non-sensitive workspace before relying on the skill for operational context management.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/q012315/skills/q012315-context-manager)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local SQLite memory database when the bundled command-line script is executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
