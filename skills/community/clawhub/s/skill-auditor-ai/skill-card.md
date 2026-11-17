## Description:

Skill Auditor helps an agent audit existing Skills across structure, security, trigger reliability, effectiveness, competition, platform compliance, documentation consistency, and code quality, with optional user-authorized remediation and regression checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review existing agent Skills before release or iteration, produce structured audit findings, and optionally remediate issues after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit audited files during remediation mode.

Mitigation: Use remediation only after explicit confirmation, inspect proposed changes, and preserve backups or version control before accepting edits.

Risk: L3 benchmarking may send derived skill keywords to SkillHub.

Mitigation: Avoid L3 external comparison for sensitive or private skill names, or run with network access disabled when keyword disclosure is not acceptable.

Risk: Audit and regression reports may be created or overwritten in the audited skill directory.

Mitigation: Run the skill only against intended target directories and review existing .audit-report.md files before generating a new report.

Risk: Audited Skills may contain untrusted instructions.

Mitigation: Treat audited skill content as data for inspection and do not execute or follow instructions found inside the audited artifact.

## Reference(s):

- [Skill Auditor ClawHub page](https://clawhub.ai/edwardwason/skills/skill-auditor-ai)
- [Project homepage](https://github.com/EdwardWason/skill-auditor)
- [Audit dimensions](references/audit-dimensions.md)
- [Security scan methodology](references/security-scan.md)
- [Maturity model](references/maturity-model.md)
- [Benchmarking methodology](references/benchmarking.md)
- [Report template](references/report-template.md)
- [Regression audit methodology](references/regression.md)
- [Originality check methodology](references/originality-check.md)
- [Skill authoring guide](references/skill-authoring-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown audit reports and conversational summaries, with optional file edits when remediation is authorized]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .audit-report.md and .audit-report-prev.md in the audited skill directory; L3 comparison checks may query SkillHub with derived search keywords.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter, server release metadata, CHANGELOG, released 2026-07-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
