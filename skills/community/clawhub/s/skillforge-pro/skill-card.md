## Description:

An audit and optimization skill for skill authors. It scores any SKILL.md across six dimensions, then returns a weighted scorecard, itemized fixes and a drop-in rewrite; in batch mode it audits a whole skill library and ranks repairs by impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjianli0721](https://clawhub.ai/user/fengjianli0721)

### License/Terms of Use:

MIT-0

## Use Case:

Skill authors and teams use it to assess a SKILL.md or skill library for trigger coverage, boundaries, workflow, acceptance checks, token size, and safety, then prioritize fixes and produce an audit report with a scorecard and rewrite or diff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan is benign with medium overall confidence, but partial coverage left some local references unresolved; the guidance also calls out detected file read/write capabilities and the lack of a declared tool scope.

Mitigation: Review the skill's file read/write behavior and confirm it fits the intended task; account for unresolved references and incomplete scan coverage before relying on the verdict.

## Reference(s):

- [audit-rubric.md](references/audit-rubric.md)
- [batch-audit.md](references/batch-audit.md)
- [rewrite-patterns.md](references/rewrite-patterns.md)
- [token-budget.md](references/token-budget.md)
- [SkillForge 技能炼金 on ClawHub](https://clawhub.ai/fengjianli0721/skills/skillforge-pro)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Diff]

**Output Format:** [Markdown audit report, JSON scorecard, and a full rewrite or per-hunk diff; batch mode also produces a Markdown repair queue.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on single or batch mode and the selected rewrite option; score-only mode omits the rewrite.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
