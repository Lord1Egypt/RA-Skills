## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory guidance for agents that evaluate their own work, catch mistakes, and improve future behavior from corrections and explicit reusable lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpjump11](https://clawhub.ai/user/jpjump11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add local correction logging, scoped preference memory, self-reflection, and conservative heartbeat maintenance to an agent workflow. It is intended for agents that should learn from explicit feedback while keeping memory visible, scoped, and reviewable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local correction and preference memory that can persistently influence future agent behavior.

Mitigation: Install only when persistent local memory is desired, keep memory visible in ~/self-improving, and periodically inspect or delete stored entries.

Risk: Setup may propose edits to AGENTS.md, SOUL.md, and HEARTBEAT.md that change how an agent behaves in the workspace.

Mitigation: Review each proposed workspace steering change before applying it and prefer Passive or Strict mode when introducing the skill.

Risk: The setup flow can offer to install a Proactivity companion skill that may require network access and is not pinned in the artifact.

Mitigation: Decline the companion unless you trust the resolved package and version, or pin and review that dependency before installation.

Risk: Long-term memory can accidentally capture sensitive or overbroad personal context if boundaries are not followed.

Mitigation: Follow the artifact's security boundaries: do not store credentials, financial data, medical data, biometrics, third-party information, location patterns, or access patterns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpjump11/skills/root)
- [Skill Homepage](https://clawic.com/skills/self-improving)
- [Setup Guide](artifact/setup.md)
- [Security Boundaries](artifact/boundaries.md)
- [Learning Mechanics](artifact/learning.md)
- [Memory Operations](artifact/operations.md)
- [Heartbeat Rules](artifact/heartbeat-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files and workspace steering suggestions; no credentials or extra binaries are required.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
