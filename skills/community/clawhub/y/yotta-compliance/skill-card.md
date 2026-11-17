## Description:

Reviews UTF-8 text and Markdown against versioned PIPL and cross-border data-transfer rules, producing evidence-linked reports for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance teams, and reviewers can use this skill to run an evidence-linked baseline review of privacy and cross-border data clauses and prepare reports for human review. It does not provide legal advice or independent conclusions for mapping-only frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and report-writing flaws can allow manipulated filesystem links to cause unintended file deletion or overwriting; reports may contain document excerpts.

Mitigation: Review before installing, use a reviewed pinned release in a fresh skill directory you control, avoid linked installation destinations, and keep reports on stdout or in a private directory. Review report excerpts before sharing.

## Reference(s):

- [Project homepage](https://github.com/YottaMeta/yotta-compliance)
- [Coverage and limitations](references/coverage.md)
- [Report format](references/report-format.md)
- [Rule authoring](references/rule-authoring.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text]

**Output Format:** [Markdown or JSON compliance review report with source excerpts, rule references, coverage labels, and review items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic rule-based results; human review is required.]

## Skill Version(s):

0.1.3 (source: SKILL.md frontmatter, CHANGELOG 2026-11-05, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
