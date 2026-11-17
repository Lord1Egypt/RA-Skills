## Description:

仓库周转与呆滞库存表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, warehouse, and operations staff use this skill during monthly close, reconciliation, or stocktaking to check warehouse turnover and slow-moving inventory tables. It recomputes supported arithmetic relationships, verifies totals, and flags duplicate, blank, placeholder, or negative values using the supplied table text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the checker output as accounting advice or as a complete inventory review.

Mitigation: Use the findings as table self-consistency checks only, then review conclusions against the organization's inventory policy, accounting requirements, and any omitted checks.

Risk: The free release omits several checks, including turnover threshold prompts, slow-moving ratio prompts, impairment reserve checks, negative ending inventory checks, and zero-issue-amount turnover checks.

Mitigation: Review the checks_not_run list before relying on results, and run additional controls or the appropriate complete workflow when those checks are required.

Risk: Incomplete or malformed table input can prevent checks from running or limit the usefulness of the findings.

Mitigation: Provide a table with the required headers and source rows; when the tool reports insufficient input, resolve the listed missing fields before drawing conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/warehouse-inventory-turnover-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, analysis, guidance]

**Output Format:** [Human-readable console text or JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows when checks run; insufficient input returns missing requirements instead of a conclusion.]

## Skill Version(s):

1.0.53 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
