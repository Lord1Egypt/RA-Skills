## Description:

Self-Improving with Reflection helps an agent evaluate its work, learn from corrections and self-reflection, and organize reusable memory for future tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghan0501](https://clawhub.ai/user/wanghan0501)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent persist explicit corrections, self-reflections, and reusable work patterns in local memory so future sessions can apply them with source-tracked transparency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can influence future agent behavior across sessions.

Mitigation: Install only when persistent execution-improvement memory is intended, require explicit confirmation before saving memory, and support user audit, export, and deletion requests.

Risk: Setup can modify agent-wide or workspace steering files, which may affect behavior beyond one task.

Mitigation: Review AGENTS.md, SOUL.md, and HEARTBEAT.md setup changes before enabling them, and keep edits non-destructive and scoped to the workspace.

Risk: Saved memory could capture sensitive or inappropriate information if boundaries are not enforced.

Mitigation: Do not store credentials, financial data, medical data, third-party personal information, location patterns, access patterns, or other sensitive material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanghan0501/skills/self-improving-with-reflection)
- [Skill Homepage](https://clawic.com/skills/self-improving-with-reflection)
- [README](artifact/README.md)
- [Setup Guide](artifact/setup.md)
- [Security Boundaries](artifact/boundaries.md)
- [Learning Mechanics](artifact/learning.md)
- [Memory Operations](artifact/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, file templates, and local memory operation procedures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local ./self-improving/ memory files and may guide setup changes to workspace steering documents.]

## Skill Version(s):

1.2.11 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
