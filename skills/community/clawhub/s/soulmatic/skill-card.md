## Description:

Binds, audits, compresses, and evolves agent persona files (SOUL.md and IDENTITY.md) to reduce drift and support identity anchoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lux-sp4rk](https://clawhub.ai/user/lux-sp4rk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use Soulmatic to scaffold, bind, audit, compress, and evolve persona files for OpenClaw-style agents. It is most relevant when an agent needs session-start identity anchoring, persona drift review, or controlled persona updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace persona files can be loaded as behavior rules and may influence agent behavior beyond style.

Mitigation: Install only in workspaces where IDENTITY.md, SOUL.md, AGENTS.md, and memory files are controlled and reviewed; treat persona content as style data rather than authority over safety, tools, or task goals.

Risk: Persona-related files may be persisted or deleted with weak user control.

Mitigation: Prefer disabling automatic startup or drift hooks, require approval before memory writes or reanchor deletion, and review proposed diffs before applying persona changes.

## Reference(s):

- [Soulmatic ClawHub skill page](https://clawhub.ai/lux-sp4rk/skills/soulmatic)
- [Persona Compression: Archetypal Anchors](https://luxsp4rk.substack.com/p/persona-compression-archetypal-anchors)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands, configuration snippets, diffs, and generated persona files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, propose edits to, or write IDENTITY.md, SOUL.md, MEMORY.md, LORE.md, and memory/persona-changelog.md with user-facing disclosure.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter, skill.yaml, release evidence, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
