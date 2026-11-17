## Description:

Smart Agent Memory provides a local long-term memory system for agents with layered context loading, per-skill experience memory, structured storage, search, reflection, and archival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyound87](https://clawhub.ai/user/beyound87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain local, searchable long-term memory for facts, lessons, entities, session summaries, and per-skill experience across OpenClaw workspaces. The CLI supports session startup and shutdown workflows, scoped recall, memory maintenance, and optional skill extraction from recorded lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command persistently adds BOOTSTRAP.md startup instructions across ~/.openclaw/workspace* directories.

Mitigation: Run setup only after review, confirm that all targeted workspaces should receive the startup instructions, and inspect BOOTSTRAP.md changes before relying on them.

Risk: Stored memory can contain secrets or untrusted instructions that may influence later agent sessions.

Mitigation: Do not store secrets or untrusted content in memory; review and sanitize memory entries before using them as context.

Risk: The extract flow can generate new skill files from remembered lessons.

Mitigation: Review generated skills and their filenames before installation or execution, especially when lesson content or skill names came from untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beyound87/skills/smart-agent-memory)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands; CLI output may be text or JSON and may create local Markdown, JSON, or SQLite-backed memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js. SQLite storage requires Node.js >= 22.5.0; otherwise the skill falls back to JSON storage.]

## Skill Version(s):

3.0.6 (source: server release metadata; source frontmatter remains 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
