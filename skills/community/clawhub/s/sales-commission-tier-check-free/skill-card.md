## Description:

Checks sales commission reconciliation tables for row-level arithmetic, total consistency, duplicates, blanks, and negative amounts, with source-backed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and payroll staff use this skill during monthly closing or commission payout review to recalculate sales commission table fields, check totals, and surface duplicate, blank, or negative entries before payments are finalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commission findings may be mistaken for final payroll or accounting decisions.

Mitigation: Review findings against the original table and the organization's commission policy before taking payroll or accounting action.

Risk: The free release does not execute every check listed by the skill.

Mitigation: Treat the report as a core arithmetic and consistency check, and review omitted checks separately when they matter.

Risk: Findings cite row and field evidence rather than full original excerpts.

Mitigation: Keep the original table available for audit and reproduce calculations before acting on a finding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/sales-commission-tier-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON check report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports insufficient input instead of drawing conclusions when required table data is missing.]

## Skill Version(s):

1.0.53 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
