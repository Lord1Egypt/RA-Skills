## Description:

Checks a VAT filing, accounting-book, and invoice reconciliation table for arithmetic mismatches, total-row errors, duplicate periods, and blank required fields, with source-cited findings for each result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during month-end closing or VAT reconciliation to compare book revenue, VAT filing sales, and invoice amounts. It reports the free-tier deterministic checks and does not replace tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on arithmetic reconciliation output as tax advice.

Mitigation: Treat results as table reconciliation only and have qualified tax or finance staff review tax-law applicability, filing decisions, and remediation steps.

Risk: The free version omits several checks, including material-difference thresholds, tax-amount cross-checks, uncommon-rate checks, and negative-value checks.

Mitigation: Review the listed checks_not_run before relying on results and run additional review for omitted controls when they matter to the filing.

Risk: Incomplete or malformed input can prevent a reliable conclusion.

Mitigation: Use the sample format, include the required headers and period rows, and treat insufficient-input output as no conclusion rather than a pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/vat-filing-reconcile-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill documentation](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON reports with source-line findings, executed checks, checks not run, and insufficient-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution; exits without a reconciliation conclusion when required input is missing or unparseable.]

## Skill Version(s):

1.0.47 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
