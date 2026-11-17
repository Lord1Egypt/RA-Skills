## Description:

增值税进销项汇总表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and tax users use this skill before monthly VAT filing to recalculate Chinese VAT input/output summary tables, totals, retained-credit carryover, duplicate periods, blanks, and burden-rate arithmetic. It reports line-numbered findings for supplied worksheet text and does not provide tax advice or filing assurance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic checks as complete tax advice or filing assurance.

Mitigation: Use the output as worksheet review support only, review the listed out-of-scope checks, and have filing decisions reviewed by qualified tax personnel.

Risk: Inputs may contain sensitive financial tax data.

Mitigation: Run the skill only on intended worksheet inputs in a trusted local environment and avoid providing unnecessary sensitive data.

Risk: The free version omits specific checks, including output-tax recalculation and burden-rate range detection.

Mitigation: Review the reported checks_withheld before relying on results, and use another control for checks outside this package.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chenqg618/skills/vat-burden-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON CLI results with line-numbered findings, summary totals, executed checks, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local deterministic worksheet checks; insufficient inputs return missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.33 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
