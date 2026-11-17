## Description:

A local deterministic checker for recruitment agency fee bills and guarantee-period refund tables that recomputes fees, refunds, totals, duplicate charges, rate caps, missing fields, placeholders, and negative values while citing source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

HR and finance teams use this skill before payment approval or month-end reconciliation to check recruitment agency fee invoices and guarantee-period refund tables. It is intended for arithmetic and table reconciliation, not legal, payroll, or contract interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can be mistaken for legal, payroll, or contract interpretation.

Mitigation: Use outputs as arithmetic and table-reconciliation support only, and have qualified reviewers confirm contract terms, payroll treatment, and legal conclusions.

Risk: Inputs can include candidate identity and compensation data.

Mitigation: Handle source tables under the organization's HR and finance data controls, and share only the minimum necessary rows with the agent workflow.

Risk: The free version explicitly omits some reconciliation checks.

Mitigation: Review the withheld-checks scope before relying on a result, especially for cross-supplier summaries, unpaid refund differences, and refund-rationale analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/recruitment-agency-fee-check-free)
- [Skill documentation](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON check results with findings, scope, and summary fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each finding is tied to a source row and candidate when enough input is available; insufficient input returns missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
