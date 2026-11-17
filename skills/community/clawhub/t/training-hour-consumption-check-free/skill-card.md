## Description:

Checks Chinese training-hour consumption and prepaid tuition reconciliation tables by recomputing row arithmetic, totals, duplicates, blanks, and negative values, with each finding tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashier staff at education and training providers use this skill during monthly close, reconciliation, or inventory checks to verify training-hour consumption and prepaid tuition tables. The free version performs its declared local checks and explicitly lists checks that are not included.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may contain sensitive student, payment, and tuition reconciliation data.

Mitigation: Run the checker locally as described by the artifact and avoid including unnecessary personal data in shared outputs.

Risk: The free version omits some checks and does not provide accounting, contract-law, tax, or refund-policy judgment.

Mitigation: Review the listed checks-not-run and have qualified staff verify financial conclusions before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/training-hour-consumption-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; optional JSON result output from the local Node.js runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing-material guidance rather than a clean conclusion.]

## Skill Version(s):

1.0.46 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
