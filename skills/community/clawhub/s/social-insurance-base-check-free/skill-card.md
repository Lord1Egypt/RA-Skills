## Description:

社保缴费基数核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。触发词包括 社保公积金缴费基数核对、社保缴费基数核对表对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, HR, and payroll staff use this skill to check social-insurance contribution base tables before monthly reconciliation or reporting. It recalculates declared amounts, checks total rows, detects duplicate or incomplete rows, and returns findings with source line evidence.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Payroll and employee contribution tables can contain sensitive employee and compensation data.

Mitigation: Run the checker only in an approved local environment and avoid sharing input files beyond the HR, payroll, or compliance workflow that requires them.

Risk: The output may be mistaken for a compliance ruling even though the tool checks internal arithmetic and table consistency.

Mitigation: Verify important payroll, HR, or compliance decisions against official local rules and treat the skill output as a reconciliation aid.

Risk: Missing headers or incomplete table data can prevent the skill from executing checks.

Mitigation: Provide the full table with recognizable headers and treat insufficient-input results as a request for more material, not as evidence that the table is correct.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/social-insurance-base-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill README](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON findings from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input must include a recognizable contribution-base table with headers; insufficient input returns missing-field guidance instead of a clean result.]

## Skill Version(s):

1.0.48 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
