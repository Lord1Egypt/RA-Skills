## Description:

Self-reflection + Self-criticism + Self-learning + Self-organizing memory for agents that evaluate their own work, catch mistakes, and improve permanently after failures, corrections, outdated knowledge, or better approaches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharemen](https://clawhub.ai/user/sharemen)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to add durable self-improvement behavior to an agent, including correction logging, scoped memory, self-reflection, heartbeat maintenance, and Chinese-adapted interaction cues. It is intended for agents that should preserve reusable lessons across sessions while keeping memory changes visible and reviewable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can influence future agent behavior across sessions.

Mitigation: Install only when durable memory is desired, keep memory entries visible, and audit stored memory on request.

Risk: Workspace steering files such as AGENTS.md, SOUL.md, and HEARTBEAT.md can change how future sessions behave.

Mitigation: Review and approve each workspace steering change separately before relying on the skill.

Risk: Memory files may accidentally contain credentials, health, financial, third-party, or sensitive personal details.

Mitigation: Do not store those categories, and remove or redact them immediately if they appear.

Risk: Export and forget-everything flows can create an additional copy of memory before deletion.

Mitigation: Treat exports as sensitive artifacts and verify deletion after wipe operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sharemen/skills/self-improving-cn)
- [Skill homepage](https://clawic.com/skills/self-improving)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown memory files and optional workspace steering files when the agent applies the skill.]

## Skill Version(s):

1.2.16 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
