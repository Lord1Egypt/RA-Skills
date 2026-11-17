## Description:

skill-optimizer analyzes, audits, and refactors SKILL.md files to improve structure, trigger behavior, clarity, and maintainability while preserving the original skill intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilifeng0-0](https://clawhub.ai/user/lilifeng0-0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review and improve SKILL.md files by applying structured agent-skill design patterns, user confirmation gates, and validation checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overly broad automatic activation can cause the skill to engage when a user only mentions skills or agents.

Mitigation: Narrow or disable broad auto-trigger terms and require an explicit request for a specific SKILL.md file before optimization.

Risk: Mutable raw main-branch installation instructions can change between review and installation.

Mitigation: Install from a pinned release or verify the published checksum before installation.

Risk: Generated optimization proposals could introduce incorrect or misleading instructions into a skill if applied without review.

Mitigation: Review generated SKILL.md changes and run project-specific validation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilifeng0-0/skills/skill-optimizer-lilifeng)
- [README-en.md](artifact/README-en.md)
- [SKILL.md](artifact/SKILL.md)
- [OPTIMIZATION_SUMMARY.md](artifact/OPTIMIZATION_SUMMARY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown containing analysis, optimized SKILL.md code blocks, change rationale, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive pipeline with user confirmation before refactoring and finalization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
