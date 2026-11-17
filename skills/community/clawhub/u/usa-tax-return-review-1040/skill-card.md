## Description:

Reviews U.S. individual Form 1040/1040-SR return data for current-year tax-rule checks, multi-year consistency, audit-risk signals, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

Tax preparers, reviewers, and agent operators use this skill to review normalized U.S. individual tax-return data, identify consistency or tax-rule issues, and prepare JSON, Markdown, and DOCX review artifacts for professional follow-up.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Generated review artifacts can contain sensitive tax-return amounts and audit-risk details.

Mitigation: Run the skill only in a trusted private workspace, write outputs to a restricted directory, and delete generated artifacts when they are no longer needed.

Risk: The optional DOCX report path depends on an unpinned python-docx install.

Mitigation: Use a virtual environment and pin python-docx before enabling DOCX generation.

Risk: Findings and audit likelihood are risk signals rather than filing advice or legal determinations.

Mitigation: Require qualified tax-professional review before using results for filing or taxpayer decisions.

## Reference(s):

- [Form 1040 Review Input Schema](references/input_schema.json)
- [Current Tax Law 2025 Parameters](references/current_tax_law_2025.json)
- [Major Items Reference](references/major_items_reference.md)
- [Example Returns](references/example_returns.json)
- [IRS Federal Income Tax Rates and Brackets](https://www.irs.gov/filing/federal-income-tax-rates-and-brackets)
- [IRS Publication 501](https://www.irs.gov/publications/p501)
- [IRS Child Tax Credit](https://www.irs.gov/credits-deductions/individuals/child-tax-credit)
- [IRS Form 8959 Instructions](https://www.irs.gov/instructions/i8959)
- [SSA Contribution and Benefit Base](https://www.ssa.gov/oact/COLA/cbbdet.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [JSON findings, Markdown summary, and DOCX risk register]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local reports to the configured output directory; DOCX output depends on python-docx unless skipped.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
