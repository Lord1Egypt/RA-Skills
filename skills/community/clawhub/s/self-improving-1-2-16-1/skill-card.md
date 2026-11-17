## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory help an agent evaluate its work, catch mistakes, and retain reusable improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyu-157](https://clawhub.ai/user/xiaoyu-157)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help an agent record explicit corrections, self-reflections, and reusable workflow lessons in local memory. It is intended for improving future task execution while preserving scoped memory, audit, export, and deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent, cross-session local memory for corrections and preferences.

Mitigation: Install only when the user accepts that behavior, review proposed memory entries, and avoid storing sensitive information.

Risk: Workspace steering changes can alter future agent behavior.

Mitigation: Review AGENTS, SOUL, and HEARTBEAT changes before accepting them, and keep inferred rules tentative until validated.

Risk: Export and deletion operations may leave retained archives unless explicitly removed.

Mitigation: Treat export and deletion workflows carefully, confirm what was removed, and inspect archives when clearing memory.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xiaoyu-157/skills/self-improving-1-2-16-1)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Skill definition](artifact/SKILL.md)
- [Setup guide](artifact/setup.md)
- [Security boundaries](artifact/boundaries.md)
- [Learning mechanics](artifact/learning.md)
- [Memory operations](artifact/operations.md)
- [Heartbeat rules](artifact/heartbeat-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory files under ~/self-improving/ and optional workspace steering files when installed.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter version 1.2.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
