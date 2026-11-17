## Description:

运单回单与代收货款核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, logistics, and operations users use this skill during monthly settlement, reconciliation, or inventory checks to verify waybill POD and COD reconciliation tables. It checks row arithmetic, totals, duplicate waybill rows within a period, blanks, placeholders, and negative values, and withholds conclusions when required table evidence is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's conclusions are limited to table arithmetic and consistency checks, not legal, accounting, tax, contract, or business-validity advice.

Mitigation: Use the findings as reconciliation support and have qualified business, accounting, or legal reviewers decide contract compliance, COD handling, tax treatment, and exception liability.

Risk: Incomplete or unrecognizable input can prevent reliable checks or hide issues outside the free edition's scope.

Mitigation: Provide the table with headers and source rows, review any insufficient-input or omitted-check messages, and separately check items listed as out of scope or not included in the free edition.

Risk: User-provided waybill, POD, and COD tables may contain sensitive commercial or customer data.

Mitigation: Run the skill only in an approved environment and limit input to the records needed for the reconciliation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/waybill-pod-cod-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON reconciliation findings with cited source rows and missing-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on user-provided table text or JSON input; material that is too incomplete to check produces an insufficient-input result rather than an all-clear conclusion.]

## Skill Version(s):

1.0.50 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
