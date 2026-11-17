## Description:

Generates evidence-based portfolio audits, candidate scorecards, privacy classifications, consolidation plans, and a persistent execution queue with dependency-linked tasks for Skill portfolio management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Skill owners and developers use this skill to inventory Skill collections, find duplicates and stale versions, prioritize workflows to package, and assess sharing risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented full-inventory workflow can enumerate private repositories account-wide, which the security scan flags as broader than a Skill portfolio audit requires; two path-like references were unresolved in the partial scan.

Mitigation: Review the repository scope and unresolved references before installation, and use authenticated all-visibility enumeration only when the audit explicitly requires it.

## Reference(s):

- [Skill Portfolio Audit on ClawHub](https://clawhub.ai/haiyangchenbj/skills/skill-portfolio-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Markdown audit report with scorecards, privacy classifications, recommendations, a roadmap, and a dependency-linked task queue]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audits existing Skills without modifying them; the persistent task queue is written to a separate ledger file.]

## Skill Version(s):

1.1.9 (source: SKILL.md frontmatter; confirmed by release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
