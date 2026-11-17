## Description:

加计抵减台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版只执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

General VAT taxpayers and their accounting or tax teams use this agent before VAT filing to check add-on deduction ledger arithmetic, totals, duplicates, blanks, and balance roll-forward relationships. It supports review of user-provided ledger text but does not decide policy eligibility, file returns, or provide tax advice.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may mistake arithmetic ledger checks for tax advice, policy eligibility decisions, or VAT filing support.

Mitigation: Use the output only as a local ledger consistency check and confirm eligibility, policy position, and filings with the主管税务机关 or qualified tax professionals.

Risk: The free release intentionally omits paid-tier checks, including some policy-ratio and eligibility-related checks.

Mitigation: Review the returned checks_not_run scope before relying on results and do not treat omitted checks as passed.

Risk: Incomplete or malformed ledger input can prevent a reliable conclusion.

Mitigation: Provide a ledger with recognizable headers and data rows; treat insufficient-input output as no conclusion rather than a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/vat-deduction-addon-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable console text or JSON results with findings, summary, scope, and cited evidence.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; input over 4 MiB is rejected; insufficient input returns missing-material guidance instead of a conclusion.]

## Skill Version(s):

1.0.22 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
