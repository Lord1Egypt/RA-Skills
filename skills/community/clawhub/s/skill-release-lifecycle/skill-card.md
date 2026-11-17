## Description:

A lightweight release-quality workflow for OpenClaw and ClawHub skills that helps agents decide publish readiness, verify releases, and turn feedback into actionable updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choosenobody](https://clawhub.ai/user/choosenobody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to evaluate OpenClaw and ClawHub skill releases before publication, verify release evidence after publication, and organize feedback into patch, versioning, or deprecation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release recommendations may be misleading when local skill files, public ClawHub pages, and release metadata disagree or cannot be checked.

Mitigation: Use server-resolved release evidence when available, identify the authoritative source before judging release quality, and label blocked or unverified checks as BLOCKED or UNCLEAR.

Risk: The workflow may lead to user-approved edits to reviewed skills or persistent global installation commands.

Mitigation: Review proposed edits and install commands before execution, then run the documented ClawHub and OpenClaw verification checks after changes.

## Reference(s):

- [ClawHub Skill Release Lifecycle Page](https://clawhub.ai/choosenobody/skills/skill-release-lifecycle)
- [SKILL.md](artifact/SKILL.md)
- [Publish Gate Worked Example](artifact/references/publish-gate-example.md)
- [Iteration Loop Worked Example](artifact/references/iteration-loop-example.md)
- [Dogfood Run 001 Self-Gate](artifact/references/dogfood-run-001-self-gate.md)
- [Dogfood Run 001 Skill Release Lifecycle](artifact/references/dogfood-run-001-skill-release-lifecycle.md)
- [Dogfood Run 002 Lifecycle Self-Evaluation](artifact/references/dogfood-run-002-lifecycle-self-eval.md)
- [Buffett-Do Mini Example](artifact/references/buffett-do-mini-example.md)
- [Dogfood Run 002 Buffett-Do](artifact/references/dogfood-run-002-buffett-do.md)
- [Session Note Skill Release Lifecycle Draft](artifact/references/session-2026-05-24-lifecycle-draft.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with checklist results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pass/fail/unclear gate findings, evidence labels, verification commands, and follow-up patch recommendations.]

## Skill Version(s):

0.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
