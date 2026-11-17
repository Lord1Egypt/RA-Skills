## Description:

Provides China individual income tax calculation and optimization assistance for salary, annual bonus, labor remuneration, special deductions, annual settlement estimates, and pre-tax to after-tax conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyue71](https://clawhub.ai/user/wangyue71)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to estimate China personal income tax, compare annual bonus tax treatments, look up special deduction rules, and produce calculation breakdowns. Outputs are estimates for planning and should be checked against current official tax guidance or a qualified tax professional.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Tax calculations may become inaccurate when tax-year rules or official guidance change.

Mitigation: Verify current rules with official tax guidance, the individual income tax app, the 12366 tax service hotline, or a qualified tax professional before relying on results.

Risk: Server security evidence says the documentation overstates some supported scenarios, including labor-income, annual-settlement, reverse salary, and other-income handling.

Mitigation: Treat those scenarios as planning estimates and avoid relying on them until the implementation gaps are fixed.

## Reference(s):

- [Personal Income Tax Rules Reference](artifact/references/tax_rules.md)
- [Salary Tax Calculator on ClawHub](https://clawhub.ai/wangyue71/skills/salary-tax-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with plain-text console summaries and optional JSON configuration input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reference-only tax estimates, calculation breakdowns, and optimization suggestions based on user-supplied income and deduction inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
